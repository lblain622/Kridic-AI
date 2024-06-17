import React,{useState} from "react";
import { Offcanvas,ListGroup,Button } from "react-bootstrap";
import fs from "fs";
export default function SessionMenu(props) {
   
    
    const [sessionList, setSessionList] = useState([]);
    const [session, setSession] = useState('');

    setSession(props.session);

    function getSessionList() {
        const chatHistoriesFolder = "FrontEnd\\chat_histories"; 
        try {
            const sessionFiles = fs.readdirSync(chatHistoriesFolder);
            const sessionNames = sessionFiles.map((file) => file.replace(".txt", ""));
            return sessionNames;
        } catch (error) {
            console.error("Error reading session files:", error);
            return [];
            }
        }
    function handleSessionClick(sessionName) {
        setSession(sessionName);
        props.onSessionSelect(sessionName);
        props.onHide();
    }
    function handleSessionDelete(sessionName) {
        const chatHistoriesFolder = "FrontEnd\\chat_histories";
        const sessionFile = `${chatHistoriesFolder}/${sessionName}.txt`;
        try {
            fs.unlinkSync(sessionFile);
            setSessionList(getSessionList());
        } catch (error) {
            console.error("Error deleting session file:", error);
        }
    }
    function renderSessionList() {
        return sessionList.map((sessionName) => (
            <ListGroup.Item key={sessionName} action onClick={() => handleSessionClick(sessionName)} active={session === sessionName}>
                {sessionName}
                <Button variant="danger" size="sm" onClick={(event) => {
                    event.stopPropagation();
                    handleSessionDelete(sessionName);
                }}>Delete</Button>
            </ListGroup.Item>
        ));
    }
    setSessionList(getSessionList());
    return (
        <Offcanvas show={props.show} onHide={props.onHide}>
            <Offcanvas.Header closeButton>
                <Offcanvas.Title>Session Menu</Offcanvas.Title>
                <Offcanvas.Body>
                    <ListGroup>
                        {renderSessionList()}
                    </ListGroup>
                </Offcanvas.Body>
            </Offcanvas.Header>
        </Offcanvas>
    )
}