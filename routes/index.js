const express=require('express');
const router = express.Router();
const homeController=require('../controllers/home_controller');
const pythonController=require('../controllers/python_controller');
router.get('/', homeController.home);
router.get('/services', homeController.services);
router.get('/contact',homeController.contact);
router.post('/contact',pythonController.home);
module.exports=router;