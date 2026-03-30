# Azure Resource Abbreviations

When naming Azure resources in documentation, Terraform configurations, architecture diagrams, or any other project
artifact, use the official abbreviation prefixes from
[Microsoft's resource abbreviation recommendations](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/azure-best-practices/resource-abbreviations).

## Quick Reference (resources used in this project)

| Resource                       | Abbreviation |
|--------------------------------|--------------|
| Resource Group                 | `rg`         |
| Function App                   | `func`       |
| Container Apps Environment     | `cae`        |
| Container App                  | `ca`         |
| PostgreSQL Database            | `psql`       |
| Azure OpenAI Service           | `oai`        |
| Foundry Hub                    | `hub`        |
| Foundry Hub Project            | `proj`       |
| Storage Account                | `st`         |
| Key Vault                      | `kv`         |
| Application Insights           | `appi`       |
| App Service Plan               | `asp`        |
| Static Web App                 | `stapp`      |
| Log Analytics Workspace        | `log`        |
| Azure Cosmos DB Database       | `cosmos`     |
| Managed Identity               | `id`         |
| Virtual Network                | `vnet`       |
| Subnet                         | `snet`       |
| Network Security Group         | `nsg`        |
| API Management                 | `apim`       |
| Azure SQL Database Server      | `sql`        |
| Azure SQL Database             | `sqldb`      |

The table above is not exhaustive. For any Azure resource type not listed here, look up the correct abbreviation in the
official Microsoft docs before naming.

## Naming Pattern

Resources follow the pattern `{abbreviation}-{project}-{environment}`, e.g., `func-omniwatcher-prod`. Storage accounts
are an exception because Azure disallows hyphens -- use `st{project}{env}` (e.g., `stomniwatcherprod`).

## When No Official Abbreviation Exists

If a resource type has no entry in the Microsoft docs, choose a short, descriptive prefix and document it in this table.
This is the only acceptable exception to using the official abbreviations.
