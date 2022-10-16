const express = require('express');
const router = express.Router();
const mongoose=require('mongoose');
const auth = require('../../middleware/auth');
const Todo = require('../../models/Todo');

// @route    GET api/listtodo
// @desc     Get all todo
// @access   Private
router.get('/', auth, async (req, res) => {
    try {
      const todos = await Todo.find({user:req.user.id});
      res.json(todos);
    } catch (err) {
      console.error(err.message);
      res.status(500).send('Server Error');
    }
  });
  
  // @route    GET api/listtodo/:id
  // @desc     Get todo by ID
  // @access   Private
  router.get('/:id', auth, async (req, res) => {
    try {
      const todo = await Todo.findById(req.params.id);
  
      // Check for ObjectId format and post
      if (!mongoose.Types.ObjectId.isValid(req.params.id) || !todo||todo.user!=req.user.id) {
        return res.status(404).json({ msg: 'Todo not found' });
      }
  
      res.json(todo);
    } catch (err) {
      console.error(err.message);
  
      res.status(500).send('Server Error');
    }
  });
  module.exports=router;