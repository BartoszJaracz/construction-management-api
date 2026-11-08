from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import Optional, Any

def get_project_dashboard(
     db: Session,
     project_id: int
     ):
     result = db.execute(
               text("""
                    SELECT * FROM vw_ProjectFullDashboard vpfd
                    WHERE vpfd.ProjectId = :project_id;
               """),
               {"project_id": project_id}
          )
          
     row = result.fetchone()
     if row is None:
          return None
     
     return dict(row._mapping)

def get_project(
     db: Session,
     project_id: int
) -> Optional[dict[str, Any]]:
     result = db.execute(
                 text("""
                     SELECT *
                     FROM Project
                     WHERE ProjectId = :project_id
                 """),
                 {"project_id": project_id}
             )
     row = result.fetchone()      
     if row is None:
          return None
     
     return dict(row._mapping)