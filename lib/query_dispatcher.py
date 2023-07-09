def dispatcher(query_type):
# All projects
    if query_type == 1:
        return """
                SELECT *
                FROM project
                INNER JOIN user_has_project ON project.project_id = user_has_project.Project_project_id
                INNER JOIN user ON project.User_project_creator = user.uid
                WHERE user_has_project.User_uid = %s
                GROUP BY project.project_id, project.project_title
                """

# Projects created by current user
    elif query_type == 2:
        return """
                SELECT *
                FROM project
                INNER JOIN user ON project.User_project_creator = user.uid
                WHERE user.uid = %s
                GROUP BY project.project_id, project.project_title
                """
# All projects sorted by starting date
    elif query_type == 3:
        return """
                SELECT *
                FROM project
                INNER JOIN user_has_project ON project.project_id = user_has_project.Project_project_id
                INNER JOIN user ON project.User_project_creator = user.uid
                WHERE user_has_project.User_uid = %s
                GROUP BY project.starting_date, project.project_title
                """
    
    # All projects sorted by ending date
    else:
        return """
                SELECT *
                FROM project
                INNER JOIN user_has_project ON project.project_id = user_has_project.Project_project_id
                INNER JOIN user ON project.User_project_creator = user.uid
                WHERE user_has_project.User_uid = %s
                GROUP BY project.ending_date, project.project_title
                """
