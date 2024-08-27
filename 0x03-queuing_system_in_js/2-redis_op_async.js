import redis from 'redis';
import { promisify } from 'util';

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

// Promisify the get function
const getAsync = promisify(client.get).bind(client);

/**
 * Function to set a value in Redis
 * @param {string} schoolName - The key to set
 * @param {string} value - The value to set
 */
function setNewSchool(schoolName, value) {
  client.set(schoolName, value, redis.print);
}

/**
 * Async function to get a value from Redis and log it
 * @param {string} schoolName - The key to retrieve
 */
async function displaySchoolValue(schoolName) {
  try {
    const value = await getAsync(schoolName);
    console.log(value);
  } catch (err) {
    console.error(err);
  }
}

// Call the functions
displaySchoolValue('Holberton');
setNewSchool('HolbertonSanFrancisco', '100');
displaySchoolValue('HolbertonSanFrancisco');
