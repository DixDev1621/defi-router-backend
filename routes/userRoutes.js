const express = require("express");
const { protect } = require("../middleware/authMiddleware");

const router = express.Router();

// protected route
router.get("/profile", protect, (req, res) => {
  res.json({ message: "This is protected profile data" });
});

module.exports = router;
