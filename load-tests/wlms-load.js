import http from "k6/http";
import { check, group } from "k6";
import { Rate } from "k6/metrics";

const errorRate = new Rate("errors");
const baseUrl = __ENV.BASE_URL || "http://127.0.0.1:8000";
const username = __ENV.WLMS_USERNAME;
const password = __ENV.WLMS_PASSWORD;

function isJsonArray(response) {
  if (response.status !== 200 || !response.body) {
    return false;
  }

  try {
    return Array.isArray(response.json());
  } catch (_error) {
    return false;
  }
}

export const options = {
  setupTimeout: "180s",
  stages: [
    { duration: "1m", target: 50 },
    { duration: "5m", target: 50 },
    { duration: "30s", target: 0 },
  ],
  thresholds: {
    http_req_failed: ["rate<0.01"],
    http_req_duration: ["avg<1000", "p(95)<2000"],
    errors: ["rate<0.01"],
  },
};

export function setup() {
  if (!username || !password) {
    throw new Error("WLMS_USERNAME and WLMS_PASSWORD are required");
  }

  const response = http.post(
    `${baseUrl}/auth/login`,
    { username, password },
    { headers: { "Content-Type": "application/x-www-form-urlencoded" } },
  );

  const validLogin = check(response, {
    "login returns 200": (r) => r.status === 200,
    "login returns a token": (r) => Boolean(r.json("access_token")),
  });
  errorRate.add(!validLogin);

  return { token: response.json("access_token") };
}

export default function (data) {
  const params = {
    headers: { Authorization: `Bearer ${data.token}` },
    timeout: "30s",
  };

  group("critical inventory reads", () => {
    const items = http.get(`${baseUrl}/items/`, params);
    const itemsOk = check(items, {
      "items returns 200": (r) => r.status === 200,
      "items returns JSON array": isJsonArray,
    });
    errorRate.add(!itemsOk);

    const stock = http.get(`${baseUrl}/stock/`, params);
    const stockOk = check(stock, {
      "stock returns 200": (r) => r.status === 200,
      "stock returns JSON array": isJsonArray,
    });
    errorRate.add(!stockOk);
  });
}

export function handleSummary(data) {
  const requestCount = data.metrics.http_reqs?.values?.count || 0;

  return {
    "load-tests/results/summary.json": JSON.stringify(data, null, 2),
    stdout: `WLMS load test completed: ${requestCount} requests\n`,
  };
}
