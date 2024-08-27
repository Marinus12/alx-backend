import kue from 'kue';

// Create a queue
const queue = kue.createQueue();

// Array containing blacklisted phone numbers
const blacklistedNumbers = [
  '4153518780',
  '4153518781'
];

// Function to handle sending notifications
function sendNotification(phoneNumber, message, job, done) {
  // Track job progress
  job.progress(0, 100);

  // Check if the phone number is blacklisted
  if (blacklistedNumbers.includes(phoneNumber)) {
    // Fail the job with a specific error message
    job.failed(new Error(`Phone number ${phoneNumber} is blacklisted`));
    return done(new Error(`Phone number ${phoneNumber} is blacklisted`));
  }

  // Track job progress to 50%
  job.progress(50, 100);

  // Log the notification details
  console.log(`Sending notification to ${phoneNumber}, with message: ${message}`);

  // Complete the job
  done();
}

// Process jobs from the queue
queue.process('push_notification_code_2', 2, (job, done) => {
  // Extract job data and call the sendNotification function
  const { phoneNumber, message } = job.data;
  sendNotification(phoneNumber, message, job, done);
});
