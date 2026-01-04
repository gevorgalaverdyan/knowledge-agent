resource "neon_project" "knowledge_assistant_project" {
  name                      = "knowledge-assistant"
  history_retention_seconds = 21600
}

resource "neon_role" "db_owner" {
  project_id = neon_project.knowledge_assistant_project.id
  branch_id  = neon_project.knowledge_assistant_project.default_branch_id
  name       = "knowledge_admin"
}

resource "neon_database" "main_db" {
  project_id = neon_project.knowledge_assistant_project.id
  branch_id  = neon_project.knowledge_assistant_project.default_branch_id
  name       = "knowledge_db"
  owner_name = neon_role.db_owner.name
}

resource "koyeb_app" "knowledge_assistant" {
  name = "knowledge-assistant-app"
}

resource "koyeb_secret" "secret_ghcr_configuration"{
  name = "GHCR_CONFIGURATION"
  type = "REGISTRY"
  github_registry {
    username = var.secret_ghcr_configuration_username
    password = var.secret_ghcr_configuration_password
  }
}

resource "koyeb_service" "backend" {
  app_name = koyeb_app.knowledge_assistant.name
  definition {
    name = "backend"
    type = "WEB"
    instance_types {
      type = "micro"
    }
    regions = ["was"]
    scalings {
      min = 1
      max = 1
    }
    ports {
      port     = 8000
      protocol = "http"
    }
    routes {
      path = "/"
      port = 8000
    }
    health_checks {
      http {
        path = "/"
        port = 8000
      }
    }
    docker {
      image = "ghcr.io/gevorgalaverdyan/knowledge-assistant-backend:latest"

    }
    env {
      key = "GEMINI_API_KEY"
      value = var.gemini_api_key
    }
    env {
      key = "GEMINI_EMBEDDING_MODEL"
      value = var.gemini_embedding_model
    }
    env {
      key = "GEMINI_GENAI_MODEL"
      value = var.gemini_genai_model
    }
    env {
      key = "DB_URL"
      value = replace(neon_project.knowledge_assistant_project.connection_uri, "postgres://", "postgresql://")
    }
    env {
      key = "AUTH0_DOMAIN"
      value = var.auth0_domain
    }
    env {
      key = "AUTH0_AUDIENCE"
      value = var.auth0_audience
    }
  }
  depends_on = [
    koyeb_app.knowledge_assistant
  ]
}
