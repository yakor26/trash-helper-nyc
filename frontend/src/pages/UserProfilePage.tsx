import { useState} from "react";
import BasicLayout from "../components/BasicLayout"
import { useAuth } from "../context/AuthContext"
import { Heading, Text, Button, Icon, HStack, VStack, Box, FormControl, InputGroup, Input, InputRightElement, InputRightAddon, IconButton, FormLabel } from "@chakra-ui/react";

import { 
    FaToggleOff,
    FaToggleOn,
    FaPhone,
    FaLock
} from "react-icons/fa";
import { IoMdAddCircle } from "react-icons/io";
import { MdEmail, MdOutlinePerson } from "react-icons/md";
import { IoLocation } from "react-icons/io5";
import { DeleteDialog } from "../components/DeleteDialog";
import { apiAuth } from "../utils/api";


export default function UserProfilePage() {

    const { user } = useAuth();
    const [addresses, setAddresses] = useState<Address[]>(user?.addresses);
    const [newAddress, setNewAddress] = useState<string>("");
    const [error, setError] = useState<string>("");
    const phoneNumber = user?.phone_number;
    const account = [
        {label: "Username", icon: MdOutlinePerson, type: user?.username},
        {label: "Email", icon: MdEmail, type: user?.email},
        {label: "Phone Number", icon: FaPhone, type: user?.phone_number},
    ]
    const handleNewAddress = async () => {
        try {
            const response = await apiAuth.post("/api/addresses", {full_address: newAddress, address_type: "residential"});
            setAddresses(prev => [...prev, response.data]);
            setNewAddress("");
        } catch (error) {
            setError("Unable to add address")

        }
    }
    const [enableNotifications, setEnableNotifications] = useState<string>(user?.allow_notifications || "false") ;
    const [isEditing, setIsEditing] = useState<boolean>(false);
 
    return (
        <>
        <BasicLayout>
        <Heading size={"lg"}>Profile Settings</Heading>
        <VStack align={"start"} spacing={6}>
        <Heading size={"md"}>Account</Heading>
         {account.map((setting) => (
            <Box bg={"gray.200"} borderRadius={"2xl"} width={"xl"} px={6} py={2} key={setting.label} position={"relative"}>
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
        <Box>{addresses.map((address) => 
            <HStack key={address.id} bg={"gray.200"} borderRadius={"2xl"} width={"xl"} px={6} py={5} my={4} position={"relative"}>
                <Icon as={IoLocation}/>
                <Text>{address.street_address}, {address.city}, {address.state}, {address.zip_code}</Text>
                <DeleteDialog address={address} addresses={addresses} setAddresses={setAddresses}/>
            </HStack> )} 
        </Box>
        : <p>Address: No address saved yet</p>}
        
        <FormControl>
            <FormLabel size={"lg"} fontWeight={"bold"}>Add an Address</FormLabel>
            <InputGroup size={"lg"} width={"xl"}>
                <Input
                placeholder="Enter Full Address"
                value={newAddress}
                size={"lg"}
                type="text"
                variant={"filled"}
                bg={"gray.200"}
                py={8}
                borderRadius={"2xl"}
                onChange={(e) => setNewAddress(e.target.value)}
                />
                <InputRightElement py={8}>
                    <IconButton
                            aria-label="delete"
                            icon={<IoMdAddCircle/>}
                            color='green'
                            bg={"transparent"}
                            size={"lg"}
                            onClick={handleNewAddress}
                        />
                </InputRightElement>
            </InputGroup>
        </FormControl>

    
        <Heading size={"md"}>Notifications</Heading>
        <Text>Text Notification Alerts: 
            {enableNotifications}
        </Text>
        
        <Button bg="brand.orange.400" fontWeight={"bold"}>Save Changes</Button>
        </VStack>
        </BasicLayout>
        </>

    )
}