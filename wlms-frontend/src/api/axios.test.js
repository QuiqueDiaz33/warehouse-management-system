import { beforeEach, describe, expect, it } from "vitest"

import api from "./axios"


describe("API client", () => {
  beforeEach(() => {
    localStorage.clear()
  })

  it("uses the local API during development", () => {
    expect(api.defaults.baseURL).toBe("http://127.0.0.1:8000")
  })

  it("does not add an authorization header without a token", async () => {
    const response = await api.get("/unit-test", {
      adapter: async (config) => ({
        data: null,
        status: 200,
        statusText: "OK",
        headers: {},
        config,
      }),
    })

    expect(response.config.headers.Authorization).toBeUndefined()
  })

  it("adds the stored token as a bearer credential", async () => {
    localStorage.setItem("token", "test-token")

    const response = await api.get("/unit-test", {
      adapter: async (config) => ({
        data: null,
        status: 200,
        statusText: "OK",
        headers: {},
        config,
      }),
    })

    expect(response.config.headers.Authorization).toBe("Bearer test-token")
  })
})

