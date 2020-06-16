#version 330

uniform samplerCube cubeMap;
uniform sampler2D modelTexture;
uniform vec4 diffuse;
uniform vec4 specular;
uniform bool UsesTexture;
uniform bool UsesLighting;
uniform bool UsesCubeMap;

in vec3 normals;
in vec4 worldPos;
in vec2 texCoord;
in vec3 cubeTexCoord;

void main() {
	// Get Texture data
	vec4 textureColor = vec4(0.0);
	if (UsesTexture) {
		if (UsesCubeMap) {
			textureColor = texture(cubeMap, cubeTexCoord);
		}
		else {
			textureColor = texture(modelTexture, texCoord);
		}
	}

	// World Position
	gl_FragData[0] = worldPos;

	// Normal
	gl_FragData[1] = vec4(normalize(normals), 1.0);

	// Diffuse Color
	if (UsesTexture) {
		gl_FragData[2] = vec4(textureColor.xyz, UsesLighting);
	}
	else {
		gl_FragData[2] = vec4(diffuse.xyz, UsesLighting);
		if (diffuse.w < 0.01) {
			discard;
		}
	}

	// Specular Color / Shininess
	gl_FragData[3] = specular;
}