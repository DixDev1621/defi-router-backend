const express = require("express");
const Project = require("../models/Project");
const { protect } = require("../middleware/authMiddleware");

const router = express.Router();

// CREATE project (protected)
router.post("/", protect, async (req, res) => {
  const project = await Project.create(req.body);
  res.json(project);
});

// READ all projects (public)
router.get("/", async (req, res) => {
  const projects = await Project.find();
  res.json(projects);
});

// UPDATE project (protected)
router.put("/:id", protect, async (req, res) => {
  const project = await Project.findByIdAndUpdate(
    req.params.id,
    req.body,
    { new: true }
  );
  res.json(project);
});

// DELETE project (protected)
router.delete("/:id", protect, async (req, res) => {
  await Project.findByIdAndDelete(req.params.id);
  res.json({ message: "Project deleted" });
});

module.exports = router;
