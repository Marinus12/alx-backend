import express from 'express';
import { createClient } from 'redis';
import { promisify } from 'util';
import kue from 'kue';

// Create a Redis client
const redisClient = createClient();
const getAsync = promisify(redisClient.get).bind(redisClient);
const setAsync = promisify(redisClient.set).bind(redisClient);

// Initialize the number of available seats and reservation status
const INITIAL_SEATS = 50;
let reservationEnabled = true;

// Function to set the number of available seats
async function reserveSeat(number) {
  await setAsync('available_seats', number);
}

// Function to get the current number of available seats
async function getCurrentAvailableSeats() {
  const seats = await getAsync('available_seats');
  return parseInt(seats, 10) || 0;
}

// Initialize available seats when the application starts
reserveSeat(INITIAL_SEATS);

// Create a Kue queue
const queue = kue.createQueue();

// Create an Express app
const app = express();

// Route to get the number of available seats
app.get('/available_seats', async (req, res) => {
  const numberOfAvailableSeats = await getCurrentAvailableSeats();
  res.json({ numberOfAvailableSeats });
});

// Route to reserve a seat
app.get('/reserve_seat', (req, res) => {
  if (!reservationEnabled) {
    return res.json({ status: 'Reservation are blocked' });
  }

  const job = queue.create('reserve_seat').save((err) => {
    if (err) {
      return res.json({ status: 'Reservation failed' });
    }
    res.json({ status: 'Reservation in process' });
  });

  job.on('complete', () => {
    console.log(`Seat reservation job ${job.id} completed`);
  });

  job.on('failed', (err) => {
    console.log(`Seat reservation job ${job.id} failed: ${err}`);
  });
});

// Route to process the queue
app.get('/process', (req, res) => {
  res.json({ status: 'Queue processing' });

  queue.process('reserve_seat', async (job, done) => {
    const availableSeats = await getCurrentAvailableSeats();

    if (availableSeats <= 0) {
      reservationEnabled = false;
      return done(new Error('Not enough seats available'));
    }

    await reserveSeat(availableSeats - 1);

    if (availableSeats - 1 === 0) {
      reservationEnabled = false;
    }

    done();
  });
});

// Start the server
app.listen(1245, () => {
  console.log('Server is running on port 1245');
});
