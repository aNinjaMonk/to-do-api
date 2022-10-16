const express = require('express');
const router = express.Router();
const mongoose=require('mongoose');
const auth = require('../../middleware/auth');
const Todo = require('../../models/Todo');

// @route    DELETE api/deletetodo
// @desc     Delete all todo
// @access   Private
router.delete('/', auth, async (req, res) => {
    try {
      const todosdeleted = await Todo.deleteMany({user:req.user.id});
      res.json(todosdeleted);
    } catch (err) {
      console.error(err.message);
      res.status(500).send('Server Error');
    }
  });
  
  // @route    DELETE api/listtodo/:id
  // @desc     Delete todo by ID
  // @access   Private
  router.delete('/:id', auth, async (req, res) => {
    try {
      const deletedtodo = await Todo.deleteOne({_id:req.params.id,user:req.user.id});
  
      // Check for ObjectId format and post
      if (!mongoose.Types.ObjectId.isValid(req.params.id) || !deletedtodo) {
        return res.status(404).json({ msg: 'Todo not found' });
      }
  
      res.json(deletedtodo);
    } catch (err) {
      console.error(err.message);
  
      res.status(500).send('Server Error');
    }
  });
  module.exports=router;