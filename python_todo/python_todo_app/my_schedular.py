from apscheduler.schedulers.blocking import BlockingScheduler

from email_sender import send_email
# from todo import ToDo  # Import the ToDo class from todo.py
from to_do import ToDo


def fetch_email():
    try:
        todo = ToDo()  # Assuming ToDo class connects to the database


        query = '''
       SELECT users.Email_id, task.Task_id, task.Title, task.Due_date
       FROM users
       INNER JOIN task ON users.id = task.User_id
       WHERE task.status='pending'
       '''

        todo.cursor.execute(query)
        tasks = todo.cursor.fetchall()
        print("all task", tasks)
        if tasks:
            print("\nPending Tasks:")
            for task in tasks:
                email = task[0]
                Task_id = task[1]
                Title = task[2]
                due_date = task[3]

                email_sent=send_email(email, Task_id, Title, due_date)
                # print ( "inside the task ")
                if email_sent:
                    # print("inside email sent")
                    update_query = '''
                                UPDATE task
                                SET status = 'Complete'
                                WHERE Task_id = %s
                                '''
                    # print(update_query)
                    todo.cursor.execute(update_query, (Task_id,))
                    todo.connection.commit()
                    print(f"Task {Task_id} marked as complete.")



                # print(f"Email: {email},task id:{Task_id},Title:{Title},Due Date:{due_date}")
        else:
            print("No pending tasks.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Close cursor and connection
        if todo.cursor:
            todo.cursor.close()
        if todo.connection:
            todo.connection.close()
scheduler = BlockingScheduler()
scheduler.add_job(fetch_email, 'interval', seconds=10)

# Start the scheduler
scheduler.start()
