#version 330 core

uniform sampler2D modelTexture;

uniform vec4 diffuse;
uniform vec3 specular;
uniform float shininess;
uniform bool UsesTexture;
uniform bool UsesLighting;

in vec3 normals;
in vec3 worldPos;
in vec2 texCoord;

uniform vec3 lightPos;
uniform vec3 eyePos;

void main() {
	vec3 diffuseTerm;
    vec3 specularTerm;

	vec4 diffuseColor = diffuse;
	if (UsesTexture) {
		diffuseColor = texture(modelTexture, texCoord);
	}

	if (UsesLighting && (diffuseColor.a >= 1.0 || UsesTexture)) {
		//Diffuse
		vec3 lightdir = normalize(lightPos - worldPos);
		vec3 norm = normalize(normals);
		float diff = max(dot(norm,lightdir),0.0);
		diffuseTerm = diff * diffuseColor.xyz;

		//Specular
		vec3 viewdir = normalize(eyePos - worldPos);
		vec3 reflectdir = reflect(-lightdir,norm);
		float spec = pow(max(dot(viewdir,reflectdir),0.0),shininess);
		specularTerm = spec * specular;

		gl_FragColor.xyz = specularTerm + diffuseTerm + 0.3 * diffuseColor.xyz;
	}
	else {
		gl_FragColor = diffuseColor;
	}
}