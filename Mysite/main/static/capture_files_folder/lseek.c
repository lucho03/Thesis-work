//------------------------------------------------------------------
// NAME: Лъчезар Иванов
// CLASS: 11„в"
// NUMBER: 10
// PROBLEM: #1
// FILE NAME: lseek.c
// FILE PURPOSE: реализация parser за абстракна блокова система, който да извежда информация на стандартния изход
//------------------------------------------------------------------
#include <stdint.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>

#include <stdio.h>
#include <unistd.h>

typedef struct{
	char data;
	unsigned char nextElementAdress;
} block;

//------------------------------------------------------------------
// FUNCTION: int main(int argc, char *argv[])
// main функция реализираща parser абстрактна блокова система, която разкодира файл example.hidden
// PARAMETERS: argc - броя на подадените аргументи на main; argv[] - аргументите на main
//------------------------------------------------------------------

int main(int argc, char *argv[]){
	int fd = open(argv[--argc], O_RDONLY);
	if(fd == -1){
		perror("a.out");
		return 1;
	}
	
	block blocks[128];
	int interpret;
	int record;
	for(int i = 0; i < 200; i++){
		interpret = read(fd, &blocks[i].data, 1);
		if(interpret == -1){
			perror("a.out");
			return 2;
		}
		
		record = write(STDOUT_FILENO, &blocks[i].data, 1);
		if(record == -1){
			perror("a.out");
			return 3;
		}
		
		interpret = read(fd, &blocks[i].nextElementAdress, 1);
		if(interpret == -1){
			perror("a.out");
			return 4;
		}
		
		if(blocks[i].nextElementAdress == 0){
			break;
		}
		lseek(fd, blocks[i].nextElementAdress, SEEK_SET);
	}
	return 0;
}
