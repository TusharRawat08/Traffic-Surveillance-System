import React, { Fragment } from 'react';
import FileUpload from '../components/FileUpload';

const Navbar=()=>{
    return <div>
    <header id="header" class="fixed-top ">
    <div class="container d-flex align-items-center justify-content-between">
    <a href="index.html" class="logo"> <img src="" alt="" class="img-fluid"></img></a>
      <nav id="navbar" class="navbar">
        
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
          <h5 className='display-4 text-center mb-4'> <b style={{color:'#5a5af3'}}>Traffic Survelliance System</b> <em style={{fontSize:'45px'}}><b style={{fontWeight:400}}> </b><em style={{color:'#d63384'}}></em>  <b style={{fontWeight:400}}></b> <b style={{color:'#5a5af3'}}>  </b> </em><b style={{fontWeight:400}}></b> </h5>
          <FileUpload />
      </div>
    </section>
  </main>
    <footer id="footer">
      <div class="container d-md-flex py-4">
  
        <div class="me-md-auto text-center text-md-start">

          <div class="credits">
      
          </div>
        </div>
   </div>
    </footer>
    <a href="#/" class="back-to-top d-flex align-items-center justify-content-center"><i class="bi bi-arrow-up-short"></i></a>  
    </div>
}
export default Navbar;