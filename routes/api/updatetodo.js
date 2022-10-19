const express = require('express');
const router = express.Router();
const { check, validationResult } = require('express-validator');
const auth = require('../../middleware/auth');
const Todo = require('../../models/Todo');


// @route    POST api/updatetodo
// @desc     Update a todo
// @access   Private
router.post(
    '/',
    [
      auth,
      [
        check('title', 'title is required')
          .not()
          .isEmpty(),
        check('details', 'details is required')
          .not()
          .isEmpty(),
        check('status', 'status is required')
          .not()
          .isEmpty(),

        check('duedate')
        // .isDate()
        .custom(value=>{ 
            let enteredDate=new Date(value);
            let todaysDate=new Date();
            if(enteredDate<=todaysDate){
                throw new Error("Invalid Date,must be in future");
            }
            return true;
        })

        
      ]
    ],
    async (req, res) => {
      const errors = validationResult(req);
      if (!errors.isEmpty()) {
        return res.status(400).json({ errors: errors.array() });
      }
  
      try {
        var updatedTodo = {
            title: req.body.title,
            details: req.body.details,
            status: req.body.status,
            duedate: req.body.duedate
        }
  
        const todo =
        await Todo.findOneAndUpdate(
            { _id: req.body.id,user:req.user.id },
            { $set: updatedTodo },
            { new: true }
          );

        res.json(todo);
      } catch (err) {
        console.error(err.message);
        res.status(500).send('Server Error');
      }
    }
  );



  module.exports=router;
  