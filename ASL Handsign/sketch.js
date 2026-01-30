console.log("🔥 Realtime ASL sketch loaded");

const sketch = (p) => {
  let video;
  let hands;
  let predictions = [];

  let table;
  let trainData = [];
  let K = 5;

  // =======================
  // LOAD DATASET
  // =======================
  p.preload = () => {
    table = p.loadTable("asl_landmarks.csv", "csv", "header",
      () => console.log("✅ CSV loaded"),
      () => console.error("❌ CSV failed")
    );
  };
function normalizeLandmarks(landmarks) {
  let wrist = landmarks[0];
  let middleTip = landmarks[12];

  let scale = p.dist(
    wrist.x, wrist.y,
    middleTip.x, middleTip.y
  );

  let normalized = [];

  for (let lm of landmarks) {
    normalized.push((lm.x - wrist.x) / scale);
    normalized.push((lm.y - wrist.y) / scale);
  }

  return normalized;
}

  p.setup = () => {
    p.createCanvas(640, 480).parent("canvas-container");
    video = p.createCapture(p.VIDEO);
    video.size(640, 480);
    video.hide();

    prepareTrainingData();

    hands = new Hands({
      locateFile: (file) => `https://cdn.jsdelivr.net/npm/@mediapipe/hands/${file}`
    });

    hands.setOptions({
      maxNumHands: 1,
      modelComplexity: 1,
      minDetectionConfidence: 0.7,
      minTrackingConfidence: 0.7
    });

    hands.onResults(onResults);

    const camera = new Camera(video.elt, {
      onFrame: async () => {
        await hands.send({ image: video.elt });
      },
      width: 640,
      height: 480
    });

    camera.start();
  };

  // =======================
  // TRAIN DATA PREP
  // =======================
  function prepareTrainingData() {
    for (let i = 0; i < table.getRowCount(); i++) {
      let row = table.getRow(i);
      let features = [];
      for (let j = 0; j < 42; j++) {
        features.push(parseFloat(row.get(j)));
      }
      trainData.push({ features, label: row.get("label") });
    }

    console.log("🧠 Training data ready:", trainData.length);
  }

  // =======================
  // MEDIAPIPE RESULT
  // =======================
    function onResults(results) {
    predictions = results.multiHandLandmarks || [];

    if (predictions.length > 0) {
        let hand = predictions[0];

        let input = normalizeLandmarks(hand);
        let result = knnPredict(input);

        document.getElementById("result").innerText = result;
    }
    }

  // =======================
  // KNN CORE
  // =======================
  function euclidean(a, b) {
    let sum = 0;
    for (let i = 0; i < a.length; i++) {
      sum += (a[i] - b[i]) ** 2;
    }
    return Math.sqrt(sum);
  }

  function knnPredict(sample) {
    let distances = trainData.map(d => ({
      label: d.label,
      dist: euclidean(sample, d.features)
    }));

    distances.sort((a, b) => a.dist - b.dist);

    let votes = {};
    for (let i = 0; i < K; i++) {
      let lbl = distances[i].label;
      votes[lbl] = (votes[lbl] || 0) + 1;
    }

    return Object.keys(votes).reduce((a, b) =>
      votes[a] > votes[b] ? a : b
    );
  }

  // =======================
  // DRAW
  // =======================
  p.draw = () => {
    p.image(video, 0, 0, p.width, p.height);

    for (let hand of predictions) {
      p.stroke(0, 255, 0);
      p.strokeWeight(2);
      p.noFill();

      for (let lm of hand) {
        p.circle(lm.x * p.width, lm.y * p.height, 10);
      }
    }
  };
};

new p5(sketch);