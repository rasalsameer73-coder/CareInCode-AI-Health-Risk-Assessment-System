const API_PREFIX = "";

function getStoredToken() {
  return localStorage.getItem("access_token");
}

function getStoredUserEmail() {
  return localStorage.getItem("user_email");
}

function getAuthHeaders() {
  const token = getStoredToken();
  if (!token) {
    return {};
  }
  return {
    Authorization: `Bearer ${token}`,
  };
}

async function request(path, options = {}) {
  const headers = {
    ...getAuthHeaders(),
    ...(options.headers || {}),
  };

  const body = options.body;
  const requestOptions = {
    method: options.method || "GET",
    headers,
    body,
  };

  if (body && !(body instanceof FormData) && !headers["Content-Type"]) {
    requestOptions.headers = {
      ...requestOptions.headers,
      "Content-Type": "application/json",
    };
  }

  const response = await fetch(`${API_PREFIX}${path}`, requestOptions);
  const contentType = response.headers.get("Content-Type") || "";
  const isJson = contentType.includes("application/json");

  let data;
  if (isJson) {
    data = await response.json();
  }

  if (!response.ok) {
    const message = data?.detail || data?.error || response.statusText || "API request failed";
    throw new Error(message);
  }

  return data;
}

export async function register({ email, password }) {
  return request("/auth/register", {
    method: "POST",
    body: JSON.stringify({ email, password }),
  });
}

export async function login({ email, password }) {
  const data = await request("/auth/login", {
    method: "POST",
    body: JSON.stringify({ email, password }),
  });
  if (data?.success && data?.access_token) {
    localStorage.setItem("access_token", data.access_token);
    localStorage.setItem("user_email", email);
  }
  return data;
}

export function logout() {
  localStorage.removeItem("access_token");
  localStorage.removeItem("user_email");
}

export function getCurrentUserEmail() {
  return getStoredUserEmail() || "demo_user";
}

export async function postVitals(vitals, userId) {
  const query = userId ? `?user_id=${encodeURIComponent(userId)}` : "";
  return request(`/analysis/vitals${query}`, {
    method: "POST",
    body: JSON.stringify(vitals),
  });
}

export async function getVitalsHistory(userId) {
  const id = userId || getCurrentUserEmail();
  return request(`/history/vitals/${encodeURIComponent(id)}`);
}

export async function uploadReport(file, userId) {
  const formData = new FormData();
  formData.append("file", file);
  const userParam = userId || getCurrentUserEmail();
  return request(`/upload/report?user_id=${encodeURIComponent(userParam)}`, {
    method: "POST",
    body: formData,
  });
}

export async function loadDoctorVisitPrep(userId) {
  const id = userId || getCurrentUserEmail();
  return request(`/doctor-visit-prep?user_id=${encodeURIComponent(id)}`);
}

export async function saveDoctorVisitPrep(payload) {
  const id = payload.user_id || getCurrentUserEmail();
  return request("/doctor-visit-prep", {
    method: "POST",
    body: JSON.stringify({
      ...payload,
      user_id: id,
    }),
  });
}

export async function getDoctorVisitPrepHistory(userId) {
  const id = userId || getCurrentUserEmail();
  return request(`/doctor-visit-prep/history/${encodeURIComponent(id)}`);
}

export async function getHistory(userId) {
  const id = userId || getCurrentUserEmail();
  return request(`/history/${encodeURIComponent(id)}`);
}
