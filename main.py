from database import get_connection


def main():
    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT version();")
                result = cursor.fetchone()

                print("Connected to PostgreSQL!!")
                print("Server Version: ", result[0])

    except (ConnectionError, ValueError) as e:
        print("Database connection failed: ", e)

    except Exception as e:
        print("Random error: ", type(e).__name__)


if __name__ == "__main__":
    main()