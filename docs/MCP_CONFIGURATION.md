# UyKelishuv Bot - MCP Configuration

## Model Context Protocol (MCP) Setup

### 1. Project Context MCP

```json
{
  "name": "uykelishuv-bot-context",
  "version": "1.0.0",
  "description": "UyKelishuv Bot project context and configuration",
  "context": {
    "project_type": "telegram_bot",
    "language": "python",
    "framework": "python-telegram-bot",
    "database": "postgresql/sqlite",
    "deployment": "railway",
    "architecture": "layered",
    "async_pattern": true
  },
  "modules": {
    "bot": {
      "description": "Telegram bot client and handlers",
      "files": [
        "src/bot/client_telegram.py",
        "src/bot/handlers/listing_handlers.py",
        "src/bot/keyboards_telegram.py"
      ],
      "dependencies": ["python-telegram-bot"]
    },
    "services": {
      "description": "Business logic layer",
      "files": [
        "src/services/user_service.py",
        "src/services/listing_service.py"
      ],
      "dependencies": ["sqlalchemy"]
    },
    "database": {
      "description": "Data access layer",
      "files": [
        "src/database/models.py",
        "src/database/database.py"
      ],
      "dependencies": ["sqlalchemy", "alembic"]
    },
    "config": {
      "description": "Configuration management",
      "files": [
        "src/config.py",
        "env.example"
      ],
      "dependencies": ["pydantic-settings"]
    }
  }
}
```

### 2. Development MCP

```json
{
  "name": "uykelishuv-bot-development",
  "version": "1.0.0",
  "description": "Development tools and workflows",
  "tools": {
    "database": {
      "migrations": "alembic",
      "commands": [
        "alembic revision --autogenerate -m 'message'",
        "alembic upgrade head",
        "alembic downgrade -1"
      ]
    },
    "testing": {
      "framework": "pytest",
      "commands": [
        "pytest tests/",
        "pytest --cov=src tests/"
      ]
    },
    "deployment": {
      "platform": "railway",
      "commands": [
        "railway login",
        "railway link",
        "railway up"
      ]
    }
  },
  "workflows": {
    "feature_development": [
      "Create feature branch",
      "Implement changes",
      "Write tests",
      "Run migrations",
      "Code review",
      "Deploy to staging",
      "Deploy to production"
    ],
    "bug_fix": [
      "Identify issue",
      "Create hotfix branch",
      "Implement fix",
      "Test fix",
      "Deploy immediately"
    ]
  }
}
```

### 3. Architecture MCP

```json
{
  "name": "uykelishuv-bot-architecture",
  "version": "1.0.0",
  "description": "System architecture and design patterns",
  "patterns": {
    "layered_architecture": {
      "presentation": "bot handlers",
      "business": "services",
      "data": "database models"
    },
    "async_pattern": {
      "description": "All operations are async",
      "benefits": ["scalability", "performance"],
      "implementation": "asyncio + asyncpg/aiosqlite"
    },
    "service_layer": {
      "description": "Business logic separation",
      "benefits": ["testability", "maintainability"],
      "implementation": "Service classes with dependency injection"
    }
  },
  "constraints": {
    "telegram_api": {
      "rate_limits": "30 messages per second",
      "file_size": "50MB max",
      "message_length": "4096 characters max"
    },
    "database": {
      "connection_pool": "max 20 connections",
      "query_timeout": "30 seconds",
      "transaction_isolation": "READ_COMMITTED"
    }
  }
}
```

### 4. Security MCP

```json
{
  "name": "uykelishuv-bot-security",
  "version": "1.0.0",
  "description": "Security policies and implementations",
  "policies": {
    "input_validation": {
      "phone_numbers": "regex: ^\\+998[0-9]{9}$",
      "text_inputs": "sanitize_html, max_length_validation",
      "file_uploads": "type_validation, size_limits"
    },
    "authentication": {
      "telegram_users": "telegram_user_id validation",
      "admin_access": "ADMIN_IDS environment variable",
      "phone_verification": "SMS-based verification"
    },
    "data_protection": {
      "sensitive_data": "encryption at rest",
      "user_privacy": "GDPR compliance",
      "audit_logging": "all user actions logged"
    }
  },
  "vulnerabilities": {
    "prevented": [
      "SQL injection",
      "XSS attacks",
      "CSRF attacks",
      "Data exposure"
    ],
    "monitoring": [
      "Failed login attempts",
      "Suspicious activity",
      "Rate limiting violations"
    ]
  }
}
```

### 5. Performance MCP

```json
{
  "name": "uykelishuv-bot-performance",
  "version": "1.0.0",
  "description": "Performance optimization guidelines",
  "metrics": {
    "response_time": {
      "target": "< 2 seconds",
      "measurement": "handler execution time"
    },
    "database": {
      "query_time": "< 500ms",
      "connection_pool": "20 max connections"
    },
    "memory": {
      "usage": "< 512MB",
      "monitoring": "heap usage tracking"
    }
  },
  "optimizations": {
    "database": [
      "Proper indexing",
      "Query optimization",
      "Connection pooling",
      "Lazy loading"
    ],
    "caching": [
      "Redis for session data",
      "In-memory caching for static data",
      "CDN for media files"
    ],
    "async": [
      "Non-blocking I/O",
      "Concurrent request handling",
      "Background task processing"
    ]
  }
}
```

### 6. Monitoring MCP

```json
{
  "name": "uykelishuv-bot-monitoring",
  "version": "1.0.0",
  "description": "Monitoring and observability setup",
  "logging": {
    "levels": ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "handlers": ["console", "file", "railway_logs"]
  },
  "metrics": {
    "user_metrics": [
      "active_users",
      "new_registrations",
      "listing_creations"
    ],
    "system_metrics": [
      "response_time",
      "error_rate",
      "database_connections"
    ],
    "business_metrics": [
      "listings_per_day",
      "search_queries",
      "contact_requests"
    ]
  },
  "alerts": {
    "critical": [
      "Bot offline",
      "Database connection failure",
      "High error rate"
    ],
    "warning": [
      "Slow response times",
      "High memory usage",
      "Rate limit approaching"
    ]
  }
}
```

### 7. Testing MCP

```json
{
  "name": "uykelishuv-bot-testing",
  "version": "1.0.0",
  "description": "Testing strategy and implementation",
  "test_types": {
    "unit_tests": {
      "scope": "individual functions and methods",
      "framework": "pytest",
      "coverage_target": "90%"
    },
    "integration_tests": {
      "scope": "service interactions",
      "framework": "pytest + testcontainers",
      "database": "test_sqlite"
    },
    "e2e_tests": {
      "scope": "complete user workflows",
      "framework": "pytest + telegram test bot",
      "scenarios": ["listing_creation", "search_flow"]
    }
  },
  "test_data": {
    "fixtures": "test_data.json",
    "mocking": "telegram_api_mocks",
    "isolation": "per_test_database_reset"
  },
  "ci_cd": {
    "pipeline": "github_actions",
    "stages": ["lint", "test", "security_scan", "deploy"],
    "environments": ["staging", "production"]
  }
}
```

### 8. Deployment MCP

```json
{
  "name": "uykelishuv-bot-deployment",
  "version": "1.0.0",
  "description": "Deployment configuration and procedures",
  "environments": {
    "development": {
      "database": "sqlite",
      "debug": true,
      "logging": "DEBUG"
    },
    "staging": {
      "database": "postgresql",
      "debug": false,
      "logging": "INFO"
    },
    "production": {
      "database": "postgresql",
      "debug": false,
      "logging": "WARNING"
    }
  },
  "railway": {
    "services": ["bot", "postgresql"],
    "environment_variables": [
      "TELEGRAM_BOT_TOKEN",
      "DATABASE_URL",
      "SECRET_KEY",
      "ADMIN_IDS"
    ],
    "deployment": "git_push_trigger"
  },
  "procedures": {
    "deployment": [
      "Run database migrations",
      "Update environment variables",
      "Deploy application",
      "Health check",
      "Monitor logs"
    ],
    "rollback": [
      "Identify issue",
      "Revert to previous version",
      "Verify functionality",
      "Update monitoring"
    ]
  }
}
```

## MCP Integration Guidelines

### Usage Instructions

1. **Load Context MCP** - Provides project overview and module information
2. **Apply Development MCP** - Sets up development tools and workflows
3. **Follow Architecture MCP** - Ensures consistent architectural patterns
4. **Implement Security MCP** - Applies security policies and validations
5. **Monitor Performance MCP** - Tracks performance metrics and optimizations
6. **Use Testing MCP** - Implements comprehensive testing strategy
7. **Execute Deployment MCP** - Manages deployment procedures

### Integration with AI Assistants

These MCPs provide structured context for AI assistants to:
- Understand project architecture and constraints
- Follow established coding patterns and standards
- Implement security best practices
- Optimize for performance requirements
- Maintain code quality and testability
- Deploy safely and reliably

### Maintenance

- Update MCPs when project requirements change
- Version control all MCP configurations
- Review and update security policies regularly
- Monitor performance metrics and adjust targets
- Keep deployment procedures current with platform changes
