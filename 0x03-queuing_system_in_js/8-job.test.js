import kue from 'kue';
import createPushNotificationsJobs from './8-job';
import { expect } from 'chai';

describe('createPushNotificationsJobs', function () {
  let queue;

  beforeEach(function () {
    queue = kue.createQueue();
    kue.testMode.enter();
  });

  afterEach(function () {
    kue.testMode.exit();
    kue.testMode.clear();
  });

  it('should display an error message if jobs is not an array', function () {
    expect(() => createPushNotificationsJobs({}, queue)).to.throw(Error, 'Jobs is not an array');
  });

  it('should create jobs in the queue', function () {
    const jobs = [
      {
        phoneNumber: '4153518780',
        message: 'This is the code 1234 to verify your account',
      },
      {
        phoneNumber: '4153518781',
        message: 'This is the code 5678 to verify your account',
      },
    ];
    
    createPushNotificationsJobs(jobs, queue);

    const jobIds = Object.keys(kue.testMode.jobs);
    expect(jobIds).to.have.lengthOf(2);
    expect(kue.testMode.jobs[jobIds[0]].type).to.equal('push_notification_code_3');
    expect(kue.testMode.jobs[jobIds[1]].type).to.equal('push_notification_code_3');
  });
});
