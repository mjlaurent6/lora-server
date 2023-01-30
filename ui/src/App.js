import logo from './logo.svg';
import './App.css';
import Paperbase from "./components/Paperbase";
import {BrowserRouter, Routes, Route} from "react-router-dom";
import Content from "./components/Content";
import Home from "./pages/Home";
import Location from "./pages/Location";
import ServerApi from "./utils/serverApi";

function App() {
    const serverApi = new ServerApi();
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<Paperbase childComponent={<Home serverApi={serverApi}/>} selectedPage={'/'}/>}/>
                <Route path="/location" element={<Paperbase childComponent={<Location serverApi={serverApi}/>}/>} selectedPage={'/location'}/>
            </Routes>
        </BrowserRouter>
    )
}

export default App;
