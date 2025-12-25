
import {assets} from "../assets"
const Footer = () => {
    return (
        <div className='text-gray-500 mt-60 text-sm pt-8 px-6 md:px-16 lg:px-24 xl:px-32'>
            <div className='flex flex-wrap justify-between items-start gap-12 pb-6 border-borderColor border-b'>
                <div>
                    <img src={assets.logo} alt="logo" className='h-8 md:h-9' />
                    <p className='max-w-80 mt-3'>
                        Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text
                    </p>
                    <div className='flex items-center gap-3 mt-6'>
                        <a href="#"><img src={assets.facebook_logo} alt="" className="w-5 h-5"/></a>
                        <a href="#"><img src={assets.instagram_logo} alt="" className="w-5 h-5"/></a>
                        <a href="#"><img src={assets.twitter_logo} alt="" className="w-5 h-5"/></a>
                        <a href="#"><img src={assets.gmail_logo} alt="" className="w-5 h-5"/></a>       
                    </div>
                </div>

                <div>
                    <h2 className='text-base font-medium text-gray-800 uppercase'>Quick links</h2>
                    <ul className='mt-3 flex flex-col gap-1.5'>
                        <li><a href="#">Home</a></li>
                        <li><a href="#">Browse Cars</a></li>
                        <li><a href="#">List your car</a></li>
                        <li><a href="#">Aboutt us</a></li>
                    </ul>
                </div>

                <div>
                    <h2 className='text-base font-medium text-gray-800 uppercase'>Resourses</h2>
                    <ul className='mt-3 flex flex-col gap-1.5'>
                        <li><a href="#">Help Center</a></li>
                        <li><a href="#">Terms of serices</a></li>
                        <li><a href="#">Privacy Policy</a></li>
                        <li><a href="#">Insurance</a></li>
                    </ul>
                </div>


                <div>
                    <h2 className='text-base font-medium text-gray-800 uppercase'>Contact</h2>
                    <ul className='mt-3 flex flex-col gap-1.5'>
                        <li>1234, Luxiru drive</li>
                        <li>Cap=Haitien , Haiti</li>
                        <li>+5095446765</li>
                        <li>luxury@gmail.com</li>
                    </ul>
                </div>

               
            </div>
            {/* <hr className='border-gray-300 mt-8' /> */}
            <div className='flex flex-col md:flex-row gap-2 items-center justify-between py-5'>
                <p>© {new Date().getFullYear()} <a href="https://prebuiltui.com">PrebuiltUI</a>. All rights reserved.</p>
                <ul className='flex items-center gap-4'>
                    <li><a href="#">Privacy</a></li>
                    <li> | </li>
                    <li><a href="#">Terms</a></li>
                    <li> | </li>
                    <li><a href="#">Cookies</a></li>
                </ul>
            </div>
        </div>
    );
};


export default Footer