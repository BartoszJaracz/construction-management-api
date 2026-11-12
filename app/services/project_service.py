from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import Optional, Any



def get_projects(db: Session) -> list[dict[str, Any]]:
     result = db.execute(
          text("SELECT * FROM Project")
     )
     
     return [
          dict(row._mapping)
          for row in result.all()
     ]

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

def get_project_dashboard(
     db: Session,
     project_id: int
     ) -> Optional[dict[str, Any]]:
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

def get_project_bottleneck(
     db: Session,
     project_id: int     
) -> Optional[dict[str, Any]]:
     result = db.execute(
          text("""
               SELECT * FROM vw_ProjectBottlenecks vpb
               WHERE vpb.ProjectId = :project_id;
          """),
          {"project_id": project_id}
     )
     row = result.fetchone()
     if row is None:
          return None
     
     return dict(row._mapping)

def create_project(
     db: Session,
     project_data: dict
) -> int:
     try:
          result = db.execute(
               text("""
                    INSERT INTO Project
                    (
                         ProjectName,
                         Scope,
                         Location,
                         Status,
                         DueDate,
                         CreatedAt
                    )
                    OUTPUT INSERTED.ProjectId
                    VALUES
                    (
                         :ProjectName,
                         :Scope,
                         :Location,
                         :Status,
                         :DueDate,
                         GETDATE()
                    )
               """),
               project_data
          )
          project_id = result.scalar()
          db.commit()
          return project_id
     
     except Exception:
          db.rollback()
          raise
     
def delete_project(
     db: Session,
     project_id: int
) -> int:
     try:
          result = db.execute(
               text("""
                    DELETE FROM Project WHERE ProjectId = :project_id;     
               """),
               {"project_id": project_id},
          )
          db.commit()
          return result.rowcount
     
     except Exception:
          db.rollback()
          raise
     
def update_project_status(
     db: Session,
     project_id: int,
     project_status_data: dict
) -> None:
     try:
          db.execute(
               text("""
                    EXEC sp_UpdateProjectStatus
                    @ProjectId = :project_id,
                    @NewStatus = :new_status;
               """),
               {
                    "project_id": project_id,
                    "new_status": project_status_data["new_status"]
               }
          )
          db.commit()
          
     except Exception:
          db.rollback()
          raise