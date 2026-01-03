output "project_connection_uri" {
  description = "Default connection URI for the primary branch (contains credentials)."
  value       = neon_project.knowledge_assistant_project.connection_uri
  sensitive   = true
}