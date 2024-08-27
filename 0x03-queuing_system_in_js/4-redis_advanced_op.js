import redis from 'redis';

// Create a Redis client
const client = redis.createClient();

// Handle the connection event
client.on('connect', () => {
  console.log('Redis client connected to the server');
});

// Handle error events
client.on('error', (err) => {
  console.error('Redis client not connected to the server:', err);
});

// Store hash values using hset
const key = 'HolbertonSchools';
client.hset(key, 'Portland', 50, redis.print);
client.hset(key, 'Seattle', 80, redis.print);
client.hset(key, 'New York', 20, redis.print);
client.hset(key, 'Bogota', 20, redis.print);
client.hset(key, 'Cali', 40, redis.print);
client.hset(key, 'Paris', 2, redis.print);

// Retrieve and display the hash using hgetall
client.hgetall(key, (err, value) => {
  if (err) {
    console.error(err);
  } else {
    console.log(value);
  }
});
