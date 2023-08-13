const express = require('express')
const router = express.Router();
module.exports.home = async function (req, res) {
  res.render('index');
};

module.exports.services = async function (req, res) {
  res.render('services');
};

module.exports.contact = async function (req, res) {
  res.render('contact');
};