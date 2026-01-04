terraform {
  required_providers {
    neon = {source="kislerdm/neon"}
    koyeb = {source="koyeb/koyeb"}
    vercel = {source="vercel/vercel"}
  }
}

provider "neon" {
  api_key = var.neon_api_key
}

provider "koyeb" {
  # tflint-ignore: all
  # api_key = var.koyeb_api_key
}
