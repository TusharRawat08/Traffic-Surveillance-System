import React, { Fragment, useState } from 'react';
import Message from './Message';
import Progress from './Progress';
import withImageLoader from 'react-image-loader-hoc';
import axios from 'axios';
const Image = props => (<img alt="" {...props} />);
const ImageWithLoader = withImageLoader(Image);
const FileUpload = () => {
  const [file, setFile] = useState('');
  const [filename, setFilename] = useState('Choose File');
  const [uploadedFile, setUploadedFile] = useState({});
  const [message, setMessage] = useState('');
  const [uploadPercentage, setUploadPercentage] = useState(0);
  const [process,setprocess]=useState(0)
  const [output_data,setoutput_data]=useState([]);
  const [res,setres]=useState([]);
  const onChange = e => {
    setFile(e.target.files[0]);
    setFilename(e.target.files[0].name);
  };
  const onSubmit = async e => {
    e.preventDefault();
    const formData = new FormData();
    formData.append('files', file);
    try {
       const res = await axios.post('http://localhost:5000/image/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        },
        onUploadProgress: progressEvent => {
          setUploadPercentage(
            parseInt(
              Math.round((progressEvent.loaded * 100) / progressEvent.total)
            )
          );
        }
      });
      setres(res.data.result)
      // Clear percentage
      const filePath = res.data.result[0].Url
      let output_data=JSON.parse(JSON.stringify(res.data.result))
      
      setoutput_data({output_data})

      setUploadPercentage(0);
      setprocess(1);
      setMessage('Uploaded')
      setUploadedFile({filePath});
    } 
    catch (err) {
    console.log(err)
    setUploadPercentage(0)
    }
  };
  return (
    <Fragment>
      {message ? <Message msg={message} /> : null}
      <form onSubmit={onSubmit}>
        <div className='custom-file mb-4'>
          <input
            type='file'
            className='custom-file-input'
            id='customFile'
            onChange={onChange}
          />
          <label className='custom-file-label' htmlFor='customFile'>
            {filename}
          </label>
        </div>

        <Progress percentage={uploadPercentage} />
        <input
          type='submit'
          value='Upload'
          className='btn btn-primary btn-block mt-4'
        />
      </form>

      {uploadedFile ? (
        <div>
        <div className='row mt-5'>
          <div className='col-md-6 m-auto'>
            <h3 className='text-center'>{uploadedFile.fileName}</h3>
            <ImageWithLoader
            src={uploadedFile.filePath} 
            width="100%"
          />
          </div>  
        </div>
        <section id="count-box" className="counts section-bg">
          <div className="container">
          
            <div className="row">
             {
              res.map((index,sub)=>{
                console.log(res[sub].Violation);
                return <div className="col-lg-3 col-md-mr-6">
                        <div className="count-box">
                          <h4 key={index}>
                            
                           <h3> Vehicle Type: {res[sub].Vehicle_Type}</h3>
                           <br></br>
                           <h5>Violations:</h5>
                           {
                             res[sub].Violation.map((v)=>{
                               return <p>
                                 <li>{v}</li>
                               </p>
                             })
                           }
                          
                          </h4>
                        </div>
                      </div>    
                })
               }
              </div>
            </div>
          </section>
        
        </div>
      ) : null}
    </Fragment>
  );
};

export default FileUpload;
