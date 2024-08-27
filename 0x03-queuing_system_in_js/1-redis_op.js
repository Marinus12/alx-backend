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

/**
 * Function to set a value in Redis
 * @param {string} schoolName - The key to set
 * @param {string} value - The value to set
 */
function setNewSchool(schoolName, value) {
  client.set(schoolName, value, redis.print);
}

/**
 * Function to get a value from Redis and log it
 * @param {string} schoolName - The key to retrieve
 */
function displaySchoolValue(schoolName) {
  client.get(schoolName, (err, value) => {
    if (err) {
      console.error(err);
      return;
    }
    console.log(value);
  });
}

// Call the functions
displaySchoolValue('Holberton');
setNewSchool('HolbertonSanFrancisco', '100');
displaySchoolValue('HolbertonSanFrancisco');
