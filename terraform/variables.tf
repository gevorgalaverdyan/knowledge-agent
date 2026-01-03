variable "neon_api_key" { 
    type = string 
    sensitive = true 
}

variable "render_api_key" { 
    type = string
    sensitive = true 
}

variable "vercel_api_key" { 
    type = string 
    sensitive = true 
}

variable "github_repo" {
  default = "https://github.com/gevorgalaverdyan/knowledge-agent"
}
