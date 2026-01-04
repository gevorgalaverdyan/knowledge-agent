variable "neon_api_key" {
  type      = string
  sensitive = true
}

variable "koyeb_api_key" {
  type      = string
  sensitive = true
}

variable "secret_ghcr_configuration_username" {
  type      = string
  sensitive = true
}

variable "secret_ghcr_configuration_password" {
  type      = string
  sensitive = true
}

variable "vercel_api_key" {
  type      = string
  sensitive = true
}

variable "github_repo" {
  default = "https://github.com/gevorgalaverdyan/knowledge-agent"
}

variable "gemini_api_key" {
  type      = string
  sensitive = true
}

variable "gemini_embedding_model" {
  type      = string
  sensitive = true
}

variable "gemini_genai_model" {
  type      = string
  sensitive = true
}

variable "auth0_domain" {
  type      = string
  sensitive = true
}

variable "auth0_audience" {
  type      = string
  sensitive = true
}
