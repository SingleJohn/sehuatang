# aioredis
import redis
# this is just example of connection.


# Create a connection
class Database:
    def __init__(self) -> None:
        self.redis = redis.ConnectionPool(host='localhost', port=6379, db=0)
    # write other methods if needed.
    