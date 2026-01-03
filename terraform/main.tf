resource "neon_project" "knowledge_assistant_project" {
  name = "knowledge-assistant"
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