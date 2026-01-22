const express = require("express");
const cors = require("cors");
require("dotenv").config();

const connectDB = require("./config/db");

// routes
const authRoutes = require("./routes/authRoutes");
const userRoutes = require("./routes/userRoutes");
const projectRoutes = require("./routes/projectRoutes");

const app = express();

// ---------- MIDDLEWARE ----------
app.use(cors());
app.use(express.json());

// ---------- DATABASE ----------
connectDB();

// ---------- ROUTES ----------
app.get("/", (req, res) => {
  res.send("Backend is running");
});

app.use("/api/auth", authRoutes);     // register, login
app.use("/api/user", userRoutes);     // profile (protected)
app.use("/api/projects", projectRoutes); // CRUD (protected + public)

// ---------- SERVER ----------
const PORT = process.env.PORT || 5000;

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
