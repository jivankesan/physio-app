import { query } from "./_generated/server";

// Define your function using query
export default query(async ({ db }) => {
  // Replace "myDataTable" with the name of your table
  return await db.query("voiceflow_feedback").collect();
});