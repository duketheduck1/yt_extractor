import React from "react";
import '../styles/index.css';
import logo from '../src/assets/logo.svg';
import Searchbar from "./Searchbar";

const Home = () => {
    return (
        <>
            <section className="px-6 md:px-20 py-40 border-2 border-red-500">
                <div className="flex max-xl:flex-col gap-16">
                    <div className="flex flex-col justify-center"> 
                        <p class="small-text">
                            Please Input your Youtube url
                        </p>
                        <h1 className="head-text">
                            Download your Youtube for 
                            <span className="text-primary"> Free</span>
                        </h1>
                        <Searchbar/>
                    </div>
                    <Download/>
                </div>
            </section>
        </>
    )
}

export default Home;