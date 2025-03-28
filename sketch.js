let data;

// 월 이름
const MONTHS = [
  "Jan",
  "Feb",
  "Mar",
  "Apr",
  "May",
  "Jun",
  "Jul",
  "Aug",
  "Sep",
  "Oct",
  "Nov",
  "Dec",
];

// 기준 anomaly 선
const REFERENCE_ANOMALIES = [-1, 0, 1, 1.5, 2];

let baseRadius;
let maxRadius;

let currentRow = 0;
let currentMonth = 0;

let prevRadius = null;
let previousAngle = null;

let lastYear;
let lastMonth;

function preload() {
  data = loadTable("glb_temp.csv", "csv", "header");
}

function setup() {
  createCanvas(windowWidth, windowHeight);

  // 반지름 계산
  let minDimension = min(windowWidth, windowHeight);
  baseRadius = minDimension * 0.1;
  maxRadius = minDimension * 0.4;

  // 마지막 연도 및 월 자동 계산
  const lastRowIndex = data.getRowCount() - 1;
  lastYear = parseInt(data.getRow(lastRowIndex).get("Year"));
  lastMonth = 11;
  for (let i = MONTHS.length - 1; i >= 0; i--) {
    if (data.getRow(lastRowIndex).get(MONTHS[i]) !== "MISSING") {
      lastMonth = i;
      break;
    }
  }

  loop();
}

function draw() {
  background(0);
  translate(width / 2, height / 2);

  drawMonthLabels();

  const year = data.getRow(currentRow).get("Year");
  drawYearLabel(year);

  drawAnomalyLines();
  drawReferenceCircles();

  currentMonth++;

  if (shouldStopAnimation(year)) {
    noLoop();
    return;
  }

  if (currentMonth === MONTHS.length) {
    currentRow++;
    currentMonth = 0;
  }

  frameRate(60);
}

// 연도 텍스트 중앙에 표시
function drawYearLabel(year) {
  textSize(baseRadius * 0.35);
  textAlign(CENTER, CENTER);
  fill(255);
  text(year, 0, 0);
}

// anomaly 데이터를 선으로 그리기
function drawAnomalyLines() {
  prevRadius = null;
  previousAngle = null;

  for (let j = 0; j <= currentRow; j++) {
    const row = data.getRow(j);
    let totalMonths = MONTHS.length;
    const year = row.get("Year");

    if (j === currentRow) {
      totalMonths = year == lastYear ? lastMonth + 1 : currentMonth;
    }

    for (let i = 0; i < totalMonths; i++) {
      const anomalyStr = row.getString(MONTHS[i]);
      if (anomalyStr === "MISSING") return;

      const anomaly = parseFloat(anomalyStr);
      if (isNaN(anomaly)) continue;

      const angle = getAngle(i);
      const radius = mapAnomalyToRadius(anomaly);

      const x1 = radius * cos(angle);
      const y1 = radius * sin(angle);

      if (previousAngle !== null) {
        const x2 = prevRadius * cos(previousAngle);
        const y2 = prevRadius * sin(previousAngle);

        stroke(getAnomalyColor(anomaly));
        strokeWeight(2);
        line(x2, y2, x1, y1);
      }

      previousAngle = angle;
      prevRadius = radius;
    }
  }
}

// anomaly 값에 따라 색상 결정
function getAnomalyColor(anomaly) {
  if (anomaly < 0) {
    return lerpColor(color(0, 0, 255), color(255), map(anomaly, -1, 0, 0, 1));
  } else {
    return lerpColor(color(255), color(255, 0, 0), map(anomaly, 0, 2, 0, 1));
  }
}

// anomaly 값을 반지름으로 매핑
function mapAnomalyToRadius(anomaly) {
  return map(
    anomaly,
    REFERENCE_ANOMALIES[0],
    REFERENCE_ANOMALIES[REFERENCE_ANOMALIES.length - 1],
    baseRadius,
    maxRadius
  );
}

// 기준선(원)과 텍스트 그리기
function drawReferenceCircles() {
  for (let i = 0; i < REFERENCE_ANOMALIES.length; i++) {
    const anomaly = REFERENCE_ANOMALIES[i];
    const radius = mapAnomalyToRadius(anomaly);

    stroke(0, 255, 0);
    strokeWeight(2);
    noFill();
    circle(0, 0, radius * 2);

    const labelX = radius + 10;
    const labelY = 0;
    textSize(baseRadius * 0.15);
    textAlign(LEFT, CENTER);
    const txt = `${anomaly}°C`;
    const txtWidth = textWidth(txt);
    const txtHeight = textAscent() + textDescent();

    fill(0, 150);
    noStroke();
    rect(labelX - 5, labelY - txtHeight / 2 - 5, txtWidth + 10, txtHeight + 10);

    fill(255);
    text(txt, labelX, labelY);
  }
}

// 월 이름 그리기
function drawMonthLabels() {
  for (let i = 0; i < MONTHS.length; i++) {
    const angle = getAngle(i);
    const x = (maxRadius + baseRadius * 0.5) * cos(angle);
    const y = (maxRadius + baseRadius * 0.5) * sin(angle);

    push();
    translate(x, y);
    rotate(angle + HALF_PI);
    noStroke();
    fill(255);
    textAlign(CENTER, CENTER);
    textSize(baseRadius * 0.22);
    text(MONTHS[i], 0, 0);
    pop();
  }
}

// 월 인덱스를 각도로 변환 (Dec가 위쪽)
function getAngle(i) {
  const adjustedIndex = (i + 1) % MONTHS.length;
  return map(adjustedIndex, 0, MONTHS.length, 0, TWO_PI) - PI / 2;
}

// 애니메이션 멈춰야 하는지 여부 판단
function shouldStopAnimation(currentYear) {
  return currentMonth > lastMonth && currentRow >= data.getRowCount() - 1;
}

// 창 크기 변경 대응
function windowResized() {
  resizeCanvas(windowWidth, windowHeight);
  const minDimension = min(windowWidth, windowHeight);
  baseRadius = minDimension * 0.1;
  maxRadius = minDimension * 0.4;
}
