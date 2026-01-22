const mongoose = require("mongoose");

const connectDB = async () => {
  try {
    await mongoose.connect("mongodb://127.0.0.1:27017/defirouter");
    console.log("MongoDB connected (LOCAL)");
  } catch (error) {
    console.error("MongoDB error:", error.message);
    process.exit(1);
  }
};

module.exports = connectDB;
