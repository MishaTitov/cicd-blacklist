// Access environment variables
const dbName = process.env.MONGO_INITDB_DATABASE;
const dbUsername = process.env.DB_USERNAME;
const dbPassword = process.env.DB_PASSWORD;

// Switch to the target database
db = db.getSiblingDB(dbName);

// Create a collection and insert documents
db.createCollection('entries');

db.entries.insertMany([
  { name: "Mike Vazowsky", reason: "Spam" },
  { name: "Gena Bukin", reason: "Fraud" },
  { name: "Ayala Morkovka", reason: "Harassment" }
]);

// Create a user with readWrite access to the database
db.createUser({
  user: dbUsername,
  pwd: dbPassword,
  roles: [
    { role: "readWrite", db: dbName }
  ]
});