import React, { Fragment } from 'react';
import FileUpload from '../components/FileUpload';

const Navbar=()=>{
    return <div>
    <header id="header" class="fixed-top ">
    <div class="container d-flex align-items-center justify-content-between">
      <a href="index.html" class="logo"> <img src="assets/img/Logo_P.png" alt="" class="img-fluid"></img></a>
      <nav id="navbar" class="navbar">
        <ul>
          <li><a class="nav-link scrollto active" href="http://vergai.in/#hero">Home</a></li>
          <li><a class="nav-link scrollto" href="http://vergai.in/#about">About</a></li>
          <li><a class="nav-link scrollto" href="http://vergai.in/course-details.html">DataeBook</a></li>
          <li><a class="nav-link scrollto" href="http://vergai.in/#portfolio">Gallery</a></li>
          <li><a class="nav-link scrollto" href="http://vergai.in/#contact">Contact</a></li>
          

          <li><a class="getstarted scrollto" href="http://18.116.148.191:3000/">Try Now</a></li>
        </ul>
        <i class="bi bi-list mobile-nav-toggle"></i>
      </nav>
    </div>
  </header>
    <main id="main">
    <section class="breadcrumbs">
      <div class="container">
        <div class="d-flex justify-content-between align-items-center">
      
        </div>
      </div>
    </section>
    <section class="inner-page">
      <div class="container">
          <h4 className='display-4 text-center mb-4'> ANPR Model</h4>
          <FileUpload />
      </div>
    </section>
  </main>
    <footer id="footer">
      <div class="container d-md-flex py-4">
  
        <div class="me-md-auto text-center text-md-start">
          <div class="copyright">
            &copy; Copyright <strong><span>VERG-AI</span></strong>. All Rights Reserved
          </div>
          <div class="credits">
      
          </div>
        </div>
        <div class="social-links text-center text-md-right pt-3 pt-md-0">
          <a href="#/" class="twitter"><i class="bx bxl-twitter"></i></a>
          <a href="#/" class="facebook"><i class="bx bxl-facebook"></i></a>
          <a href="#/" class="instagram"><i class="bx bxl-instagram"></i></a>
          <a href="#/" class="google-plus"><i class="bx bxl-skype"></i></a>
          <a href="#/" class="linkedin"><i class="bx bxl-linkedin"></i></a>
        </div>
      </div>
    </footer>
    <a href="#/" class="back-to-top d-flex align-items-center justify-content-center"><i class="bi bi-arrow-up-short"></i></a>  
    </div>
}
export default Navbar;