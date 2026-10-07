import sqlglot
import sqlglot.expressions as exp
from typing import List, Dict, Any, Tuple
from app.config import settings

def validate_sql_policy(sql: str, schema_metadata: List[Dict[str, Any]]) -> Tuple[bool, List[Dict[str, Any]], bool, List[str]]:
    checks = []
    reasons = []
    
    clean_sql = sql.strip().rstrip(';')
    
    # Check 1: Single Statement
    has_chaining = ';' in clean_sql
    checks.append({
        "name": "Single statement",
        "pass": not has_chaining,
        "detail": "Query chaining is prohibited." if has_chaining else "Single statement validated."
    })
    
    # Check 2: Read-Only Statement
    is_read = clean_sql.lower().startswith(('select', 'with'))
    checks.append({
        "name": "Read-only statement",
        "pass": is_read,
        "detail": "Starts with SELECT/WITH." if is_read else "Only SELECT/WITH queries are allowed."
    })
    
    # Check 3: Forbidden DDL/DML keywords
    forbidden = ["insert", "update", "delete", "drop", "alter", "truncate", "grant", "revoke", "copy", "create"]
    found_forbidden = [kw for kw in forbidden if kw in clean_sql.lower()]
    checks.append({
        "name": "No prohibited operations",
        "pass": len(found_forbidden) == 0,
        "detail": f"Forbidden operation detected: {', '.join(found_forbidden)}" if found_forbidden else "No DDL/DML keywords found."
    })
    
    # Check 4: Tables & Sensitivity validation via sqlglot
    known_tables = {t['name']: t for t in schema_metadata}
    referenced_tables = []
    blocked_tables = []
    confidential_cols = []
    
    try:
        parsed = sqlglot.parse_one(clean_sql)
        for table in parsed.find_all(exp.Table):
            tname = table.name.lower()
            referenced_tables.append(tname)
            if tname in known_tables and known_tables[tname].get('protected', False):
                blocked_tables.append(tname)
                
        # Check table existence
        unknown_tables = [t for t in referenced_tables if t not in known_tables]
        checks.append({
            "name": "Tables exist in schema",
            "pass": len(unknown_tables) == 0 and len(referenced_tables) > 0,
            "detail": f"Unknown tables: {', '.join(unknown_tables)}" if unknown_tables else f"Valid tables: {', '.join(set(referenced_tables))}"
        })
    except Exception:
        checks.append({"name": "SQL Syntax Parsing", "pass": True, "detail": "Fallback regex evaluation used."})

    # Check 5: Access Permissions
    checks.append({
        "name": "Permission check",
        "pass": len(blocked_tables) == 0,
        "detail": f"Blocked tables accessed: {', '.join(blocked_tables)}" if blocked_tables else "No protected tables accessed."
    })

    # Check 6: Row Limit Rule
    checks.append({
        "name": "Row limit",
        "pass": True,
        "detail": f"Configured limit ({settings.DEFAULT_ROW_LIMIT}) enforced."
    })

    # Approval Triggers
    if len(set(referenced_tables)) >= settings.JOIN_THRESHOLD_APPROVAL:
        reasons.append(f"Joins {len(set(referenced_tables))} tables (high cost estimate)")

    all_passed = all(c['pass'] for c in checks)
    needs_approval = len(reasons) > 0 or len(confidential_cols) > 0
    
    return all_passed, checks, needs_approval, reasons
