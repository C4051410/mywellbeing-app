from database.connection import connect

def retrieve_users_moderators(search_query=""):
    #connects to database
    conn = connect()
    try:
        cur = conn.cursor()
        #query used to merge both foodlog and workouts, using source to distinguish
        query = """
                SELECT * FROM (SELECT f.title, u.username, f.id, 'food' as source \
                               FROM foodlog f \
                                        JOIN users u ON f.user_id = u.id \
                               UNION ALL \
                               SELECT w.title, u.username, w.id, 'work' as source \
                               FROM workouts w \
                                        JOIN users u ON w.user_id = u.id)
                    AS combined
        """
        params = []
        #used for searching for specific user
        if search_query:
            query += " WHERE username ILIKE %s"
            params.extend([f"%{search_query}%"])
        #execute query
        cur.execute(query, tuple(params))
        #return all results
        rows = cur.fetchall()
        conn.close()
        cur.close()
        return rows
    except Exception as e:
        print(e)
        conn.close()

def delete_posts_moderator(post_id:int, source:str):
    conn = connect()
    try:
        cur = conn.cursor()
        #checks if source is food
        if source == "food":
            #deletes from food
            cur.execute("DELETE FROM foodlog WHERE id = %s", (post_id,))
        #else if would be work
        elif source == "work":
            cur.execute("DELETE FROM workouts WHERE id = %s", (post_id,))
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(e)
        #undos any actions if error occurred
        conn.rollback()
        conn.close()