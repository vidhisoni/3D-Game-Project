#version 330 core

uniform vec4 diffuse;

void main() {
	gl_FragColor = diffuse;
}