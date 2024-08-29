import React, { useState } from 'react';
import { View, TextInput, Button, Text, StyleSheet, Dimensions,TouchableOpacity } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import axios from 'axios';

const { width, height } = Dimensions.get('window');

const LoginScreen = ({ navigation }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleLogin = async () => {
    try {
      // Obtener el CSRF token
      const csrfResponse = await axios.get('http://localhost:8000/csrf-token/');
      const csrfToken = csrfResponse.data.csrfToken;

      console.log("Obtenido CSRF token: ", csrfToken);

      // Verificar que el CSRF token está presente
      if (!csrfToken) {
        throw new Error('CSRF token is missing.');
      }

      // Realizar la solicitud de login
      const response = await axios.post('http://localhost:8000/clogin', 
        { 
          username: username,
          password: password,
        }, // Datos del cuerpo de la solicitud
        { 
          headers: {
            'X-CSRFToken': csrfToken,
            'Content-Type': 'application/json'
          },
          withCredentials: true // Asegúrate de que esta opción esté habilitada si estás usando cookies
        }
      );
      
      const { access } = response.data;
      const { user } = response.data;
      console.log("Respuesta de login: ", response.data);
      console.log("user: ",user);
      console.log("user.username: ",user.username);
      console.log("user.id: ",user.id);

      if (access) {
        // Guardar el token en AsyncStorage
        await AsyncStorage.setItem('access_token', access);
        await AsyncStorage.setItem('username', user.username);
        await AsyncStorage.setItem('id', user.id);
        console.log("Token guardado en AsyncStorage: ", access);

        // Navegar a la pantalla principal
        navigation.replace('AppTabs');
      } else {
        console.error('No se recibió el token de acceso.');
      }
    } catch (error) {
      console.log("error en catch login: ", error);
      setError('Error al iniciar sesión. Verifica tus credenciales.');
    }
  };

  return (
    <View style={styles.container}>
      <View style={styles.formContainer}>
        <Text style={styles.title}>Iniciar sesión</Text>
        <TextInput
          style={styles.input}
          placeholder="Username"
          value={username}
          onChangeText={setUsername}
        />
        <TextInput
          style={styles.input}
          placeholder="Password"
          secureTextEntry
          value={password}
          onChangeText={setPassword}
        />
        {error ? <Text style={styles.error}>{error}</Text> : null}
        <TouchableOpacity onPress={handleLogin} style={styles.button}>
          <Text style={styles.buttonText}>Login</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
    backgroundColor: '#FF7F50', 
  },
  formContainer: {
    width: '100%',
    maxWidth: 400, 
    backgroundColor: 'white',
    padding: 20,
    borderRadius: 10,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.3,
    shadowRadius: 5,
    elevation: 5,
  },
  title: {
    fontSize: 24, // Tamaño del texto
    fontWeight: 'bold', // Negrita
    textAlign: 'center', // Centrado
    marginBottom: 20, // Espacio debajo del título
  },
  input: {
    height: 40,
    borderColor: '#ddd',
    borderWidth: 1,
    marginBottom: 15,
    paddingHorizontal: 10,
    borderRadius: 5,
  },
  button: {
    marginTop: 10,
    padding: 10,
    backgroundColor: '#BDB76B',
    borderRadius: 5,
  },
  
  buttonText: {
    color: 'white',
    textAlign: 'center',
  },
  error: {
    color: 'red',
    marginBottom: 10,
  },
});

export default LoginScreen;