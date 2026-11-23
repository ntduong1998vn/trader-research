import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import test from 'node:test';
import { Indicator, PineTS, localTimeToUTC } from 'pinets';

// Execute the shipped Pine source, not a JavaScript copy of its trading rules.
// PineTS is a third-party engine; these tests do not certify TradingView compilation.
const source = readFileSync(new URL('../pine/orb-entry-indicator.pine', import.meta.url), 'utf8');
const MINUTE = 60_000;
const DAY = 86_400_000;
const ZONE = 'America/New_York';
const ambiguity = 'Không rõ thứ tự trong nến';
const missing = 'Thiếu dữ liệu khi đang theo dõi';
const defaults = { 'Phiên liên tục': '0930-0942' };

function session(date = '2026-11-16', { minutes = 12, start = '09:30', volume = 100, colour = 'green', or = 5 } = {}) {
  const begin = localTimeToUTC(date, start, ZONE);
  return Array.from({ length: minutes }, (_, i) => ({
    openTime: begin + i * MINUTE,
    closeTime: begin + (i + 1) * MINUTE,
    open: i < or ? 100 : 100.5,
    high: i < or ? 101 : 100.8,
    low: i < or ? 99 : 100.3,
    close: i < or ? (colour === 'green' ? 100.5 : colour === 'red' ? 99.5 : 100) : 100.5,
    volume,
  }));
}

function candle(bars, i, open, high, low, close) {
  Object.assign(bars[i], { open, high, low, close });
  return bars;
}

function buy(bars, i = 5) {
  return candle(bars, i, 100.5, 101.3, 100.5, 101.2);
}

function dailyBars(bars) {
  const lastDate = new Date(bars.at(-1).openTime).toISOString().slice(0, 10);
  return Array.from({ length: 45 }, (_, i) => {
    const date = new Date(Date.parse(lastDate) - (44 - i) * DAY).toISOString().slice(0, 10);
    return {
      openTime: localTimeToUTC(date, '09:30', ZONE),
      closeTime: localTimeToUTC(date, '16:00', ZONE),
      open: 100, high: 101, low: 99, close: 100, volume: 1000,
    };
  });
}

async function run(bars, inputs = {}, { daily = dailyBars(bars), timeframe = '1', ticker = 'TEST:ORB' } = {}) {
  const provider = {
    async getMarketData(_symbol, tf) {
      assert.ok(tf === timeframe || tf === '1D', `Unexpected request ${tf}`);
      return tf === '1D' ? daily : bars;
    },
    async getSymbolInfo() {
      return {
        tickerid: 'TEST:ORB', timezone: ZONE, mintick: 0.01, minmove: 1,
        pricescale: 100, session: '0930-1600', type: 'stock',
      };
    },
    configure() {},
  };
  const engine = new PineTS(provider, ticker, timeframe);
  engine.setAlertMode('all');
  const result = await engine.run(new Indicator(source, { ...defaults, ...inputs }));
  assert.deepEqual(result.warnings, [], 'PineTS runtime warnings');
  return result;
}

function values(result, name) {
  assert.ok(result.plots[name], `Missing plot: ${name}`);
  return result.plots[name].data.map(({ value }) => value);
}

function events(result, name) {
  return values(result, name).flatMap((value, i) => value === true ? [i] : []);
}

function level(result, name, i) {
  const odd = values(result, name)[i];
  return Number.isFinite(odd) ? odd : values(result, `${name} (2)`)[i];
}

for (const minutes of [5, 15, 30, 60]) {
  test(`OR ${minutes} minutes locks before the first eligible entry`, async () => {
    const bars = session(undefined, { minutes: minutes + 5, or: minutes });
    buy(bars, minutes);
    candle(bars, minutes + 1, 101.2, 120, 90, 101.2);
    const end = new Date(bars.at(-1).closeTime).toLocaleTimeString('en-GB', { timeZone: ZONE, hour: '2-digit', minute: '2-digit' }).replace(':', '');
    const result = await run(bars, { 'Số phút đầu phiên': minutes, 'Phiên liên tục': `0930-${end}` });
    assert.deepEqual(events(result, 'Entry mua'), [minutes]);
    assert.ok(values(result, 'Đỉnh OR').slice(0, minutes - 1).every(Number.isNaN));
    assert.ok(values(result, 'Đỉnh OR').slice(minutes - 1).every(v => v === 101));
    assert.ok(values(result, 'Đáy OR').slice(minutes - 1).every(v => v === 99));
  });
}

test('Classic ignores a wick; Paper uses the complete green OR candle', async () => {
  const bars = session();
  // The first minute is red, but the complete five-minute OR is green.
  bars[0].close = 99.5;
  candle(bars, 5, 100.95, 101.1, 100.9, 100.95);
  const classic = await run(bars);
  const paper = await run(bars, { 'Cách vào': 'Paper' });
  assert.deepEqual(events(classic, 'Entry mua'), []);
  assert.deepEqual(events(paper, 'Entry mua'), [5]);
  assert.equal(level(paper, 'Giá entry tham chiếu', 5), 101);
  assert.equal(level(paper, 'Dừng lỗ', 5), 100.8);
  assert.ok(Number.isNaN(level(paper, 'Mục tiêu', 5)));
});

test('Paper red OR sells; a doji OR skips the session', async () => {
  const red = session(undefined, { colour: 'red' });
  candle(red, 5, 99.05, 99.1, 98.9, 99.05);
  assert.deepEqual(events(await run(red, { 'Cách vào': 'Paper' }), 'Entry bán'), [5]);
  const doji = buy(session(undefined, { colour: 'doji' }));
  const result = await run(doji, { 'Cách vào': 'Paper' });
  assert.deepEqual(events(result, 'Entry mua'), []);
  assert.deepEqual(events(result, 'Entry bán'), []);
});

test('Classic short is symmetric and respects the selected side', async () => {
  const bars = session();
  candle(bars, 5, 99.5, 99.6, 98.7, 98.8);
  const result = await run(bars);
  assert.deepEqual(events(result, 'Entry bán'), [5]);
  assert.equal(level(result, 'Dừng lỗ', 5), 101);
  assert.equal(level(result, 'Mục tiêu', 5), 96.6);
  assert.deepEqual(events(await run(bars, { 'Chiều cho phép': 'Chỉ mua' }), 'Entry bán'), []);
  assert.deepEqual(events(await run(buy(session()), { 'Chiều cho phép': 'Chỉ bán' }), 'Entry mua'), []);
});

test('Paper fills a gap at the open, not the OR edge', async () => {
  const bars = session();
  candle(bars, 5, 101.5, 101.6, 101.4, 101.5);
  const result = await run(bars, { 'Cách vào': 'Paper' });
  assert.equal(level(result, 'Giá entry tham chiếu', 5), 101.5);
  assert.equal(level(result, 'Dừng lỗ', 5), 101.3);
  assert.deepEqual(events(result, 'Entry mua'), [5]);
  assert.equal(values(result, 'Giá thoát tham chiếu')[6], 100.5);
});

test('Paper intrabar touch and stop remain ambiguous if the close cannot prove order', async () => {
  const bars = session();
  candle(bars, 5, 100.9, 101.1, 100.7, 100.9);
  const result = await run(bars, { 'Cách vào': 'Paper' });
  assert.deepEqual(events(result, 'Entry mua'), [5]);
  assert.deepEqual(events(result, ambiguity), [5]);
  assert.deepEqual(events(result, 'Chạm stop'), []);
  assert.ok(Number.isNaN(values(result, 'Giá thoát tham chiếu')[5]));
});

test('Paper close beyond stop proves a same-bar stop, long and short', async () => {
  const long = session();
  candle(long, 5, 100.9, 101.1, 100.6, 100.7);
  const longResult = await run(long, { 'Cách vào': 'Paper' });
  assert.deepEqual(events(longResult, 'Chạm stop'), [5]);
  assert.deepEqual(events(longResult, ambiguity), []);
  assert.equal(values(longResult, 'Giá thoát tham chiếu')[5], 100.8);
  const short = session(undefined, { colour: 'red' });
  candle(short, 5, 99.1, 99.4, 98.9, 99.3);
  const shortResult = await run(short, { 'Cách vào': 'Paper' });
  assert.deepEqual(events(shortResult, 'Chạm stop'), [5]);
  assert.equal(values(shortResult, 'Giá thoát tham chiếu')[5], 99.2);
});

test('Paper entry at the open followed by a stop is not ambiguous', async () => {
  const bars = session();
  candle(bars, 5, 101.2, 101.4, 100.9, 101.1);
  const result = await run(bars, { 'Cách vào': 'Paper' });
  assert.deepEqual(events(result, 'Chạm stop'), [5]);
  assert.deepEqual(events(result, ambiguity), []);
  assert.equal(values(result, 'Giá thoát tham chiếu')[5], 101);
});

test('Classic only checks stop/target after the entry candle', async () => {
  const bars = buy(session());
  bars[5].low = 98;
  const result = await run(bars);
  assert.deepEqual(events(result, 'Entry mua'), [5]);
  assert.deepEqual(events(result, 'Chạm stop'), []);
  assert.deepEqual(events(result, 'Đóng cuối phiên'), [11]);
  assert.equal(values(result, 'Giá thoát tham chiếu')[11], bars[11].close);
});

test('Classic flags simultaneous stop/target without inventing an exit price', async () => {
  const bars = buy(session());
  candle(bars, 6, 101.2, 104, 98, 101.2);
  const result = await run(bars);
  assert.deepEqual(events(result, ambiguity), [6]);
  assert.deepEqual(events(result, 'Chạm stop'), []);
  assert.deepEqual(events(result, 'Chạm target'), []);
  assert.ok(Number.isNaN(values(result, 'Giá thoát tham chiếu')[6]));
});

for (const [open, title] of [[98, 'Chạm stop'], [105, 'Chạm target']]) {
  test(`Classic opening gap resolves ${title} before other touches`, async () => {
    const bars = buy(session());
    candle(bars, 6, open, 106, 97, 101.2);
    const result = await run(bars);
    assert.deepEqual(events(result, title), [6]);
    assert.equal(values(result, 'Giá thoát tham chiếu')[6], open);
    assert.deepEqual(events(result, ambiguity), []);
  });
}

test('Classic can disable its target and use closed daily ATR for the stop', async () => {
  const bars = buy(session());
  const result = await run(bars, { 'Classic: vẽ mục tiêu': false, 'Classic: dừng lỗ': '10% ATR ngày' });
  assert.equal(level(result, 'Dừng lỗ', 5), 101);
  assert.ok(Number.isNaN(level(result, 'Mục tiêu', 5)));
});

test('Last candle blocks new Classic entries but closes a Paper entry', async () => {
  const bars = session();
  candle(bars, 11, 100.95, 101.1, 100.9, 101.05);
  assert.deepEqual(events(await run(bars), 'Entry mua'), []);
  const paper = await run(bars, { 'Cách vào': 'Paper' });
  assert.deepEqual(events(paper, 'Entry mua'), [11]);
  assert.deepEqual(events(paper, 'Đóng cuối phiên'), [11]);
  assert.equal(values(paper, 'Giá thoát tham chiếu')[11], 101.05);
});

test('One-entry default and optional Classic re-entry use separate level channels', async () => {
  const bars = buy(session());
  candle(bars, 6, 101.2, 101.3, 98.8, 100.5);
  buy(bars, 7);
  assert.deepEqual(events(await run(bars), 'Entry mua'), [5]);
  const result = await run(bars, { 'Classic: tối đa 1 entry / phiên': false });
  assert.deepEqual(events(result, 'Entry mua'), [5, 7]);
  assert.ok(Number.isFinite(values(result, 'Dừng lỗ')[6]));
  assert.ok(Number.isNaN(values(result, 'Dừng lỗ')[7]));
  assert.ok(Number.isNaN(values(result, 'Dừng lỗ (2)')[6]));
  assert.ok(Number.isFinite(values(result, 'Dừng lỗ (2)')[7]));
});

test('New sessions reset the one-entry limit without needing extended-hours bars', async () => {
  const result = await run([...buy(session()), ...buy(session('2026-11-17'))]);
  assert.deepEqual(events(result, 'Entry mua'), [5, 17]);
  assert.deepEqual(events(result, 'Đóng cuối phiên'), [11, 23]);
});

test('RVOL excludes today and requires all prior samples before filtering', async () => {
  const bars = [
    ...buy(session(undefined, { volume: 100 })),
    ...buy(session('2026-11-17', { volume: 200 })),
    ...buy(session('2026-11-18', { volume: 600 })),
  ];
  const result = await run(bars, { 'Bật lọc RVOL': true, 'Số phiên OR trước': 2, 'RVOL tối thiểu': 3.9 });
  assert.ok(values(result, 'RVOL của OR').slice(0, 28).every(Number.isNaN));
  assert.equal(values(result, 'RVOL của OR')[28], 4);
  assert.deepEqual(events(result, 'Entry mua'), [29]);
  const blocked = await run(bars, { 'Bật lọc RVOL': true, 'Số phiên OR trước': 2, 'RVOL tối thiểu': 4.1 });
  assert.deepEqual(events(blocked, 'Entry mua'), []);
});

for (const badVolume of [NaN, 0]) {
  test(`RVOL excludes a ${String(badVolume)}-volume opening window`, async () => {
    const first = buy(session());
    if (Number.isNaN(badVolume)) first[2].volume = NaN;
    else first.slice(0, 5).forEach(bar => { bar.volume = 0; });
    const bars = [...first, ...buy(session('2026-11-17')), ...buy(session('2026-11-18'))];
    const result = await run(bars, { 'Bật lọc RVOL': true, 'Số phiên OR trước': 1 });
    assert.deepEqual(events(result, 'Entry mua'), [29]);
    assert.equal(values(result, 'RVOL của OR')[28], 1);
  });
}

test('A partially loaded session or a missing OR candle cannot signal', async () => {
  const partial = buy(session()).slice(1);
  assert.deepEqual(events(await run(partial), 'Entry mua'), []);
  const gap = buy(session()).filter((_, i) => i !== 2);
  assert.deepEqual(events(await run(gap), 'Entry mua'), []);
});

test('A gap after OR invalidates the rest of the session, even before entry', async () => {
  const bars = buy(session(), 7).filter((_, i) => i !== 5);
  assert.deepEqual(events(await run(bars), 'Entry mua'), []);
});

test('Missing bars during a trade flag DATA without inventing an exit', async () => {
  const bars = buy(session()).filter((_, i) => i !== 6);
  const result = await run(bars);
  assert.deepEqual(events(result, missing), [6]);
  assert.deepEqual(events(result, 'Đóng cuối phiên'), []);
  assert.ok(values(result, 'Giá thoát tham chiếu').every(Number.isNaN));
});

test('A missing final candle is reported on the next received candle, never backdated', async () => {
  const bars = [...buy(session()).slice(0, -1), ...session('2026-11-17')];
  const result = await run(bars);
  assert.deepEqual(events(result, missing), [11]);
  assert.deepEqual(events(result, 'Đóng cuối phiên'), []);
  assert.ok(values(result, 'Giá thoát tham chiếu').every(Number.isNaN));
});

test('New York session anchors follow DST changes', async () => {
  const before = buy(session('2026-03-06'));
  const after = buy(session('2026-03-09'));
  assert.equal(new Date(before[0].openTime).getUTCHours(), 14);
  assert.equal(new Date(after[0].openTime).getUTCHours(), 13);
  const result = await run([...before, ...after]);
  assert.deepEqual(events(result, 'Entry mua'), [5, 17]);
});

test('An overnight session crosses midnight and month end without resetting OR', async () => {
  const bars = buy(session('2026-10-31', { start: '23:55', minutes: 15 }));
  const result = await run(bars, { 'Phiên liên tục': '2355-0010', 'Ngày: 1=CN, 2=T2, ..., 7=T7': '1234567' });
  assert.deepEqual(events(result, 'Entry mua'), [5]);
  assert.deepEqual(events(result, 'Đóng cuối phiên'), [14]);
  assert.equal(values(result, 'Đỉnh OR')[14], 101);
});

test('Daily ATR ignores the current daily candle, even if its range changes massively', async () => {
  const bars = buy(session());
  const daily = dailyBars(bars);
  daily.at(-1).high = 1000;
  daily.at(-1).low = 1;
  const result = await run(bars, { 'Cách vào': 'Paper' }, { daily });
  assert.ok(values(result, 'ATR ngày đã đóng').every(v => v === 2));
  assert.equal(level(result, 'Dừng lỗ', 5), 100.8);
  const insufficient = await run(bars, { 'Cách vào': 'Paper' }, { daily: daily.slice(-5) });
  assert.deepEqual(events(insufficient, 'Entry mua'), []);
  assert.deepEqual(events(await run(bars, {}, { daily: daily.slice(-5) }), 'Entry mua'), [5]);
});

test('Historical entry plots are not limited by retained OR boxes', async () => {
  const bars = Array.from({ length: 45 }, (_, i) => {
    const date = new Date(Date.UTC(2026, 8, 1 + i)).toISOString().slice(0, 10);
    return buy(session(date));
  }).flat();
  const result = await run(bars, { 'Số hộp OR giữ lại': 1, 'Ngày: 1=CN, 2=T2, ..., 7=T7': '1234567' });
  assert.equal(events(result, 'Entry mua').length, 45);
  assert.equal(events(result, 'Entry mua')[0], 5);
});

test('Appending later candles does not change confirmed earlier signals or levels', async () => {
  const bars = buy(session());
  const prefix = await run(bars.slice(0, 8));
  const full = await run(bars);
  for (const name of ['Entry mua', 'Entry bán', 'Đỉnh OR', 'Đáy OR', 'Dừng lỗ', ambiguity]) {
    assert.deepEqual(values(prefix, name), values(full, name).slice(0, 8), name);
  }
  assert.deepEqual(full.alerts.filter(a => a.title === 'ORB mua').map(a => a.bar_index), [5]);
});

test('An unconfirmed final candle does not create an entry', async () => {
  const bars = buy(session()).slice(0, 6);
  bars[5].closeTime = Date.now() + MINUTE;
  assert.deepEqual(events(await run(bars), 'Entry mua'), []);
});

for (const [options, inputs] of [
  [{ timeframe: '5' }, {}],
  [{ ticker: 'TEST:ORB;heikinashi' }, {}],
  [{}, { 'Ngày: 1=CN, 2=T2, ..., 7=T7': '0' }],
  [{}, { 'Ngày: 1=CN, 2=T2, ..., 7=T7': '' }],
]) {
  test(`Rejects unsupported chart/session input ${JSON.stringify({ options, inputs })}`, async () => {
    await assert.rejects(run(session(), inputs, options), /Chỉ dùng|Ngày giao dịch/);
  });
}
