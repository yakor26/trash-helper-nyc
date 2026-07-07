import { useState } from "react";
import BasicLayout from "../components/BasicLayout"
import { useAuth } from "../context/AuthContext"
import { Heading, Text, Button, Icon, HStack, VStack, Box } from "@chakra-ui/react";
import { 
    FaToggleOff,
    FaToggleOn,
    FaPhone
} from "react-icons/fa";
import { MdEmail, MdOutlinePerson } from "react-icons/md";
import { IoLocation } from "react-icons/io5";


export default function UserProfilePage() {
    const { user } = useAuth();
    const addresses = user?.addresses
    const phoneNumber = user?.phone_number;
    const account = [
        {label: "Username", icon: MdOutlinePerson, type: user?.username},
        {label: "Email", icon: MdEmail, type: user?.email},
        {label: "Phone Number", icon: FaPhone, type: user?.phone_number},
    ]
    const [enableNotifications, setEnableNotifications] = useState<string>(user?.allow_notifications || "false") ;
    const [isEditing, setIsEditing] = useState<boolean>(false);
    return (
        <>
        <BasicLayout>
        <Heading size={"lg"}>Profile Settings</Heading>
        <VStack align={"start"} spacing={4}>
        <Heading size={"md"}>Account</Heading>
         {account.map((setting) => (
            <Box bg={"gray.200"} borderRadius={"2xl"} width={"sm"} px={6} py={2} key={setting.label} position={"relative"}>
            <HStack>
                <Icon as={setting.icon}/>
                <Text fontWeight={"bold"}>{setting.label}</Text>
                {!isEditing ?
                <Button onClick={() => setIsEditing(true)} position={"absolute"} right={2} top={2}>Edit</Button>
                : <Button onClick={() => setIsEditing(false)} position={"absolute"} right={2} top={2}>Save</Button>
                }
            </HStack>
            {!isEditing ? <Text>{setting.type}</Text> : <Text>Edit State</Text>}

        </Box>
            
        ))}

        <Heading size={"md"}>Saved Addresses</Heading>
        {addresses ? 
        <p>{addresses.map((address) => 
            <li key={address.id}>
                <Icon as={IoLocation}/>
                {address.street_address}, {address.city}, {address.state}, {address.zip_code}
            </li> )} </p> 
        : <p>Address: No address saved yet</p>}
    
        <Heading size={"md"}>Notifications</Heading>
        <Text>Text Notification Alerts: 
            {enableNotifications}
        </Text>
        
        <Button>Save Changes</Button>
        </VStack>
        </BasicLayout>
        </>

    )
}