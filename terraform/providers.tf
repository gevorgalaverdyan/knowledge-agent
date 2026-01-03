terraform {
  required_providers {
    neon = {source="kislerdm/neon"}
    render = {source="render-oss/render"}
    vercel = {source="vercel/vercel"}
  }
}

provider "neon" {
  api_key = var.neon_api_key
}
